from rest_framework import viewsets, filters, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.conf import settings as django_settings
from django.template.loader import render_to_string
from django.db.models import Count, Sum, Avg, Q
from django.db.models.functions import TruncDay, TruncMonth

from .models import Article, Category, Tag, Source, Media, RawNews, NewsletterSubscriber, Comment, SitePage, SiteSettings
from .serializers import (
    ArticleListSerializer,
    ArticleDetailSerializer,
    ArticleCreateUpdateSerializer,
    CategorySerializer,
    TagSerializer,
    SourceSerializer,
    MediaSerializer,
    RawNewsSerializer,
    NewsletterSubscriberSerializer,
    CommentSerializer,
    CommentCreateSerializer,
    SitePageSerializer,
    SiteSettingsSerializer,
)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.select_related(
        'category', 'source'
    ).prefetch_related('tags', 'media')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'is_featured', 'is_breaking', 'category', 'category__slug']
    search_fields = ['title', 'content', 'meta_title', 'meta_description']
    ordering_fields = ['created_at', 'updated_at', 'published_at', 'view_count', 'title']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        elif self.action == 'retrieve':
            return ArticleDetailSerializer
        return ArticleCreateUpdateSerializer

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        article = self.get_object()
        article.status = 'publie'
        article.published_at = timezone.now()
        article.save()
        self._notify_subscribers(article)
        return Response({'status': 'published'})

    def _notify_subscribers(self, article):
        try:
            subscribers = list(
                NewsletterSubscriber.objects.filter(is_active=True).values_list('email', flat=True)
            )
            if not subscribers:
                return
            frontend_url = getattr(django_settings, 'FRONTEND_URL', 'http://localhost:5173')
            excerpt = (article.content or '')[:200]
            subject = f'[GNEWZ] {article.title}'
            text_body = (
                f'{article.title}\n\n'
                f'{excerpt}...\n\n'
                f'Read more: {frontend_url}\n\n'
                f'---\nUnsubscribe: {frontend_url}/unsubscribe'
            )
            html_body = render_to_string('articles/newsletter_email.html', {
                'article_title': article.title,
                'article_excerpt': f'{excerpt}...',
                'article_slug': article.slug,
                'frontend_url': frontend_url,
            })
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_body,
                from_email=django_settings.DEFAULT_FROM_EMAIL,
                to=subscribers,
            )
            msg.attach_alternative(html_body, "text/html")
            msg.send(fail_silently=True)
        except Exception:
            pass

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        article = self.get_object()
        article.status = 'archive'
        article.save()
        return Response({'status': 'archived'})

    @action(detail=True, methods=['post'])
    def increment_view(self, request, pk=None):
        article = self.get_object()
        article.view_count += 1
        article.save(update_fields=['view_count'])
        return Response({'view_count': article.view_count})


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'slug']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type']
    search_fields = ['name', 'slug']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'is_active']
    search_fields = ['name', 'url']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class RawNewsViewSet(viewsets.ModelViewSet):
    queryset = RawNews.objects.select_related('source')
    serializer_class = RawNewsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'source']
    search_fields = ['title', 'content', 'url']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'], url_path='urls')
    def urls(self, request):
        urls = RawNews.objects.exclude(url__isnull=True).exclude(url='').values_list('url', flat=True)
        return Response({'urls': urls})

    @action(detail=False, methods=['post'], url_path='bulk-delete')
    def bulk_delete(self, request):
        ids = request.data.get('ids', [])
        if not ids:
            return Response({'error': 'No IDs provided.'}, status=status.HTTP_400_BAD_REQUEST)
        deleted, _ = RawNews.objects.filter(id__in=ids).delete()
        return Response({'deleted': deleted})

    @action(detail=False, methods=['post'], url_path='bulk-status')
    def bulk_status(self, request):
        ids = request.data.get('ids', [])
        new_status = request.data.get('status', '')
        valid = [c[0] for c in RawNews.STATUS_CHOICES]
        if not ids or new_status not in valid:
            return Response({'error': 'Invalid IDs or status.'}, status=status.HTTP_400_BAD_REQUEST)
        updated = RawNews.objects.filter(id__in=ids).update(status=new_status)
        return Response({'updated': updated})


class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['alt_text', 'caption', 'credit']
    ordering_fields = ['created_at']
    ordering = ['-created_at']


class SendEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '').strip()
        if not email:
            return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

        frontend_url = getattr(django_settings, 'FRONTEND_URL', 'http://localhost:5173')
        text_body = (
            f'Hello,\n\n'
            f'This is a test email from GNEWZ.\n\n'
            f'Visit us at: {frontend_url}\n'
        )
        html_body = render_to_string('articles/newsletter_email.html', {
            'article_title': 'Welcome to GNEWZ',
            'article_excerpt': 'Your go-to source for gaming and esports news. Stay ahead of every play.',
            'article_slug': '',
            'frontend_url': frontend_url,
        })

        try:
            msg = EmailMultiAlternatives(
                subject='[GNEWZ] Test Email',
                body=text_body,
                from_email=django_settings.DEFAULT_FROM_EMAIL,
                to=[email],
            )
            msg.attach_alternative(html_body, "text/html")
            msg.send()
        except Exception as e:
            return Response({'error': f'Failed to send email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': f'Email sent to {email}.'}, status=status.HTTP_200_OK)


class NewsletterSubscribeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '').strip()
        if not email:
            return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)
        subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
        if not created and subscriber.is_active:
            return Response({'message': 'Already subscribed.'}, status=status.HTTP_200_OK)
        subscriber.is_active = True
        subscriber.save()

        return Response({'message': 'Subscribed successfully.'}, status=status.HTTP_201_CREATED)


# ---------------------------------------------------------------------------
# Statistics APIs
# ---------------------------------------------------------------------------

class GlobalStatsView(APIView):
    """GET /api/stats/ — dashboard overview counts."""

    def get(self, request):
        from accounts.models import User

        total_articles = Article.objects.count()
        published_articles = Article.objects.filter(status='publie').count()
        total_views = Article.objects.aggregate(total=Sum('view_count'))['total'] or 0

        return Response({
            'articles': {
                'total': total_articles,
                'published': published_articles,
                'draft': Article.objects.filter(status='brouillon_ia').count(),
                'in_review': Article.objects.filter(status='en_revision').count(),
                'archived': Article.objects.filter(status='archive').count(),
                'featured': Article.objects.filter(is_featured=True).count(),
                'breaking': Article.objects.filter(is_breaking=True).count(),
            },
            'raw_news': {
                'total': RawNews.objects.count(),
                'nouveau': RawNews.objects.filter(status='nouveau').count(),
                'traite': RawNews.objects.filter(status='traite').count(),
                'ignore': RawNews.objects.filter(status='ignore').count(),
            },
            'sources': {
                'total': Source.objects.count(),
                'active': Source.objects.filter(is_active=True).count(),
                'inactive': Source.objects.filter(is_active=False).count(),
            },
            'categories': {'total': Category.objects.count()},
            'tags': {'total': Tag.objects.count()},
            'media': {'total': Media.objects.count()},
            'newsletter': {
                'total': NewsletterSubscriber.objects.count(),
                'active': NewsletterSubscriber.objects.filter(is_active=True).count(),
            },
            'users': {
                'total': User.objects.count(),
                'admins': User.objects.filter(user_type='admin').count(),
                'editors': User.objects.filter(user_type='editor').count(),
                'viewers': User.objects.filter(user_type='viewer').count(),
            },
            'total_views': total_views,
        })


class ArticleStatsView(APIView):
    """GET /api/stats/articles/ — detailed article statistics."""

    def get(self, request):
        # Articles by status
        by_status = list(
            Article.objects.values('status').annotate(count=Count('id')).order_by('status')
        )

        # Articles by category
        by_category = list(
            Article.objects.filter(category__isnull=False)
            .values('category__id', 'category__name', 'category__slug')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        # Top 10 most viewed articles
        top_viewed = list(
            Article.objects.filter(status='publie')
            .order_by('-view_count')
            .values('id', 'title', 'slug', 'view_count', 'published_at')[:10]
        )

        # Articles published per day (last 30 days)
        thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
        by_day = list(
            Article.objects.filter(published_at__gte=thirty_days_ago)
            .annotate(day=TruncDay('published_at'))
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )

        # Articles published per month (last 12 months)
        twelve_months_ago = timezone.now() - timezone.timedelta(days=365)
        by_month = list(
            Article.objects.filter(published_at__gte=twelve_months_ago)
            .annotate(month=TruncMonth('published_at'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )

        # Views per day (last 30 days) — approximated from published articles
        total_views = Article.objects.aggregate(total=Sum('view_count'))['total'] or 0
        avg_views = Article.objects.filter(status='publie').aggregate(avg=Avg('view_count'))['avg'] or 0

        return Response({
            'by_status': by_status,
            'by_category': by_category,
            'top_viewed': top_viewed,
            'published_by_day': by_day,
            'published_by_month': by_month,
            'total_views': total_views,
            'avg_views_per_article': round(avg_views, 2),
        })


class SourceStatsView(APIView):
    """GET /api/stats/sources/ — articles and raw news per source."""

    def get(self, request):
        by_type = list(
            Source.objects.values('type').annotate(count=Count('id')).order_by('type')
        )

        per_source_articles = list(
            Source.objects.annotate(article_count=Count('articles'))
            .values('id', 'name', 'type', 'is_active', 'article_count')
            .order_by('-article_count')
        )

        per_source_raw = list(
            Source.objects.annotate(raw_count=Count('raw_news'))
            .values('id', 'name', 'type', 'is_active', 'raw_count')
            .order_by('-raw_count')
        )

        return Response({
            'by_type': by_type,
            'articles_per_source': per_source_articles,
            'raw_news_per_source': per_source_raw,
        })


class RawNewsStatsView(APIView):
    """GET /api/stats/raw-news/ — raw news processing statistics."""

    def get(self, request):
        by_status = list(
            RawNews.objects.values('status').annotate(count=Count('id')).order_by('status')
        )

        by_source = list(
            RawNews.objects.filter(source__isnull=False)
            .values('source__id', 'source__name')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        by_day = list(
            RawNews.objects.annotate(day=TruncDay('created_at'))
            .values('day')
            .annotate(count=Count('id'))
            .order_by('-day')[:30]
        )

        return Response({
            'by_status': by_status,
            'by_source': by_source,
            'ingested_by_day': by_day,
        })


class CategoryStatsView(APIView):
    """GET /api/stats/categories/ — articles per category."""

    def get(self, request):
        stats = list(
            Category.objects.annotate(
                article_count=Count('articles'),
                published_count=Count('articles', filter=Q(articles__status='publie')),
            )
            .values('id', 'name', 'slug', 'article_count', 'published_count')
            .order_by('-article_count')
        )
        return Response({'categories': stats})


class TagStatsView(APIView):
    """GET /api/stats/tags/ — top tags by article usage."""

    def get(self, request):
        by_type = list(
            Tag.objects.values('type').annotate(count=Count('id')).order_by('type')
        )

        top_tags = list(
            Tag.objects.annotate(article_count=Count('articles'))
            .values('id', 'name', 'slug', 'type', 'article_count')
            .order_by('-article_count')[:50]
        )

        return Response({'by_type': by_type, 'top_tags': top_tags})


class NewsletterStatsView(APIView):
    """GET /api/stats/newsletter/ — subscriber statistics."""

    def get(self, request):
        total = NewsletterSubscriber.objects.count()
        active = NewsletterSubscriber.objects.filter(is_active=True).count()

        by_month = list(
            NewsletterSubscriber.objects.annotate(month=TruncMonth('subscribed_at'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )

        return Response({
            'total': total,
            'active': active,
            'unsubscribed': total - active,
            'subscriptions_by_month': by_month,
        })


class UserStatsView(APIView):
    """GET /api/stats/users/ — user account statistics."""

    def get(self, request):
        from accounts.models import User

        by_type = list(
            User.objects.values('user_type').annotate(count=Count('id')).order_by('user_type')
        )

        by_month = list(
            User.objects.annotate(month=TruncMonth('date_joined'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )

        return Response({
            'total': User.objects.count(),
            'active': User.objects.filter(is_active=True).count(),
            'by_type': by_type,
            'registrations_by_month': by_month,
        })


# ---------------------------------------------------------------------------
# Site Settings API  (singleton — GET / PATCH /api/settings/)
# ---------------------------------------------------------------------------

class SiteSettingsView(APIView):
    """
    GET   /api/settings/  — retrieve current settings (admin only)
    PATCH /api/settings/  — update settings (admin only)
    """

    def get(self, request):
        settings = SiteSettings.load()
        return Response(SiteSettingsSerializer(settings).data)

    def patch(self, request):
        if not request.user.is_authenticated or request.user.user_type not in ('admin', 'editor'):
            return Response({'error': 'Admin or editor access required.'}, status=status.HTTP_403_FORBIDDEN)
        settings = SiteSettings.load()
        serializer = SiteSettingsSerializer(settings, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# ---------------------------------------------------------------------------
# Site Pages API
# ---------------------------------------------------------------------------

class SitePageViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    GET  /api/pages/         — list all pages (public)
    GET  /api/pages/{slug}/  — retrieve page content (public)
    PATCH /api/pages/{slug}/ — update page content (admin/editor only)
    """
    queryset = SitePage.objects.all()
    serializer_class = SitePageSerializer
    lookup_field = 'slug'


# ---------------------------------------------------------------------------
# Comment APIs
# ---------------------------------------------------------------------------

class ArticleCommentListCreateView(APIView):
    """
    GET  /api/articles/{article_id}/comments/  — list top-level comments + replies
    POST /api/articles/{article_id}/comments/  — add a comment (public)
    """
    permission_classes = [AllowAny]

    def _get_article(self, article_id):
        try:
            return Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            return None

    def get(self, request, article_id):
        article = self._get_article(article_id)
        if not article:
            return Response({'error': 'Article not found.'}, status=status.HTTP_404_NOT_FOUND)

        comments = (
            Comment.objects
            .filter(article=article, parent__isnull=True)
            .prefetch_related('replies')
            .order_by('created_at')
        )
        serializer = CommentSerializer(comments, many=True)
        return Response({
            'article_id': article.id,
            'count': comments.count(),
            'comments': serializer.data,
        })

    def post(self, request, article_id):
        article = self._get_article(article_id)
        if not article:
            return Response({'error': 'Article not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        comment = serializer.save(
            article=article,
            author=request.user if request.user.is_authenticated else None,
        )
        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)


class ArticleCommentDetailView(APIView):
    """
    DELETE /api/articles/{article_id}/comments/{comment_id}/ — admin only
    """

    def _get_comment(self, article_id, comment_id):
        try:
            return Comment.objects.get(pk=comment_id, article_id=article_id)
        except Comment.DoesNotExist:
            return None

    def delete(self, request, article_id, comment_id):
        if not request.user.is_authenticated or request.user.user_type != 'admin':
            return Response({'error': 'Admin access required.'}, status=status.HTTP_403_FORBIDDEN)

        comment = self._get_comment(article_id, comment_id)
        if not comment:
            return Response({'error': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
