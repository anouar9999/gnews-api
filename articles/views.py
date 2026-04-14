from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.conf import settings as django_settings
from django.db.models import Count, Sum, Avg, Q
from django.db.models.functions import TruncDay, TruncMonth

from .models import Article, Category, Tag, Source, Media, RawNews, NewsletterSubscriber, Comment
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
            html_body = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin:0;padding:0;background:#0d0d0d;font-family:'Segoe UI',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#0d0d0d;padding:48px 0;">
    <tr>
      <td align="center">
        <table width="580" cellpadding="0" cellspacing="0" style="max-width:580px;width:100%;">

          <!-- Logo -->
          <tr>
            <td align="center" style="padding-bottom:28px;">
              <span style="color:#FF6B00;font-size:26px;font-weight:800;letter-spacing:3px;text-transform:uppercase;">GNEWZ</span>
            </td>
          </tr>

          <!-- Card -->
          <tr>
            <td style="background:#1a1a1a;border-radius:12px;overflow:hidden;border:1px solid #2a2a2a;">

              <!-- Icon banner -->
              <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td align="center" style="padding:36px 32px 24px;">
                    <div style="display:inline-block;background:#FF6B00;border-radius:50%;width:56px;height:56px;text-align:center;line-height:56px;font-size:26px;">&#128240;</div>
                  </td>
                </tr>

                <!-- Headline -->
                <tr>
                  <td align="center" style="padding:0 32px 12px;">
                    <h1 style="color:#ffffff;font-size:32px;font-weight:800;margin:0;letter-spacing:-0.5px;">Breaking News Alert</h1>
                  </td>
                </tr>

                <!-- Subheading -->
                <tr>
                  <td align="center" style="padding:0 40px 32px;">
                    <p style="color:#9ca3af;font-size:15px;line-height:1.6;margin:0;">A new story just dropped on GNEWZ. Stay ahead of every play.</p>
                  </td>
                </tr>

                <!-- Divider -->
                <tr>
                  <td style="padding:0 32px;">
                    <div style="height:1px;background:#2a2a2a;"></div>
                  </td>
                </tr>

                <!-- Article title -->
                <tr>
                  <td style="padding:28px 32px 8px;">
                    <p style="color:#FF6B00;font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin:0 0 10px;">Latest Article</p>
                    <h2 style="color:#ffffff;font-size:20px;font-weight:700;margin:0 0 14px;line-height:1.4;">{article.title}</h2>
                    <p style="color:#9ca3af;font-size:14px;line-height:1.7;margin:0 0 28px;">{excerpt}...</p>
                  </td>
                </tr>

                <!-- CTA Button -->
                <tr>
                  <td align="center" style="padding:0 32px 36px;">
                    <a href="{frontend_url}" style="display:inline-block;background:#FF6B00;color:#ffffff;text-decoration:none;padding:14px 36px;border-radius:6px;font-size:15px;font-weight:700;letter-spacing:0.5px;">Read Full Article &rarr;</a>
                  </td>
                </tr>

                <!-- Features row -->
                <tr>
                  <td style="background:#111111;padding:28px 32px;border-top:1px solid #2a2a2a;">
                    <table width="100%" cellpadding="0" cellspacing="0">
                      <tr>
                        <td width="33%" align="center" style="padding:0 8px;">
                          <p style="color:#FF6B00;font-size:18px;margin:0 0 6px;">&#9889;</p>
                          <p style="color:#ffffff;font-size:13px;font-weight:700;margin:0 0 4px;">Live Updates</p>
                          <p style="color:#6b7280;font-size:11px;line-height:1.5;margin:0;">Breaking stories as they happen</p>
                        </td>
                        <td width="33%" align="center" style="padding:0 8px;border-left:1px solid #2a2a2a;border-right:1px solid #2a2a2a;">
                          <p style="color:#FF6B00;font-size:18px;margin:0 0 6px;">&#127942;</p>
                          <p style="color:#ffffff;font-size:13px;font-weight:700;margin:0 0 4px;">Esports Coverage</p>
                          <p style="color:#6b7280;font-size:11px;line-height:1.5;margin:0;">Tournaments, teams &amp; results</p>
                        </td>
                        <td width="33%" align="center" style="padding:0 8px;">
                          <p style="color:#FF6B00;font-size:18px;margin:0 0 6px;">&#127918;</p>
                          <p style="color:#ffffff;font-size:13px;font-weight:700;margin:0 0 4px;">Game Reviews</p>
                          <p style="color:#6b7280;font-size:11px;line-height:1.5;margin:0;">In-depth analysis &amp; scores</p>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>

              </table>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td align="center" style="padding:24px 0 8px;">
              <p style="color:#4b5563;font-size:12px;margin:0 0 6px;">
                You're receiving this because you subscribed to GNEWZ gaming news.
              </p>
              <a href="{frontend_url}/unsubscribe" style="color:#6b7280;font-size:12px;text-decoration:underline;">Unsubscribe</a>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""
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
        html_body = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin:0;padding:0;background:#0d0d0d;font-family:'Segoe UI',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#0d0d0d;padding:48px 0;">
    <tr>
      <td align="center">
        <table width="580" cellpadding="0" cellspacing="0" style="max-width:580px;width:100%;">

          <!-- Logo -->
          <tr>
            <td align="center" style="padding-bottom:28px;">
              <span style="color:#FF6B00;font-size:26px;font-weight:800;letter-spacing:3px;text-transform:uppercase;">GNEWZ</span>
            </td>
          </tr>

          <!-- Card -->
          <tr>
            <td style="background:#1a1a1a;border-radius:12px;overflow:hidden;border:1px solid #2a2a2a;">
              <table width="100%" cellpadding="0" cellspacing="0">

                <!-- Icon -->
                <tr>
                  <td align="center" style="padding:44px 32px 20px;">
                    <div style="display:inline-block;background:#FF6B00;border-radius:50%;width:60px;height:60px;text-align:center;line-height:60px;font-size:28px;">&#128293;</div>
                  </td>
                </tr>

                <!-- Headline -->
                <tr>
                  <td align="center" style="padding:0 32px 10px;">
                    <h1 style="color:#ffffff;font-size:36px;font-weight:800;margin:0;letter-spacing:-1px;">You're In.</h1>
                  </td>
                </tr>

                <!-- Subheading -->
                <tr>
                  <td align="center" style="padding:0 48px 36px;">
                    <p style="color:#9ca3af;font-size:16px;line-height:1.6;margin:0;">Let's get you up to speed on everything gaming &amp; esports.</p>
                  </td>
                </tr>

                <!-- CTA Button -->
                <tr>
                  <td align="center" style="padding:0 32px 44px;">
                    <a href="{frontend_url}" style="display:inline-block;background:#FF6B00;color:#ffffff;text-decoration:none;padding:14px 40px;border-radius:6px;font-size:15px;font-weight:700;letter-spacing:0.5px;">Explore GNEWZ &rarr;</a>
                  </td>
                </tr>

                <!-- Divider -->
                <tr>
                  <td style="padding:0 32px;">
                    <div style="height:1px;background:#2a2a2a;"></div>
                  </td>
                </tr>

                <!-- Features -->
                <tr>
                  <td style="background:#111111;padding:32px;">
                    <table width="100%" cellpadding="0" cellspacing="0">

                      <!-- Feature 1 -->
                      <tr>
                        <td style="padding-bottom:24px;">
                          <table cellpadding="0" cellspacing="0">
                            <tr>
                              <td style="width:40px;vertical-align:top;padding-top:2px;">
                                <div style="background:#FF6B00;border-radius:50%;width:32px;height:32px;text-align:center;line-height:32px;font-size:15px;">&#9889;</div>
                              </td>
                              <td style="padding-left:14px;">
                                <p style="color:#ffffff;font-size:14px;font-weight:700;margin:0 0 4px;">Breaking Esports News</p>
                                <p style="color:#6b7280;font-size:13px;line-height:1.5;margin:0;">Live scores, roster moves, and tournament results — the moment they happen.</p>
                              </td>
                            </tr>
                          </table>
                        </td>
                      </tr>

                      <!-- Feature 2 -->
                      <tr>
                        <td style="padding-bottom:24px;">
                          <table cellpadding="0" cellspacing="0">
                            <tr>
                              <td style="width:40px;vertical-align:top;padding-top:2px;">
                                <div style="background:#FF6B00;border-radius:50%;width:32px;height:32px;text-align:center;line-height:32px;font-size:15px;">&#127942;</div>
                              </td>
                              <td style="padding-left:14px;">
                                <p style="color:#ffffff;font-size:14px;font-weight:700;margin:0 0 4px;">Optimized for Every Screen</p>
                                <p style="color:#6b7280;font-size:13px;line-height:1.5;margin:0;">Read on web, desktop, or mobile — GNEWZ looks great everywhere.</p>
                              </td>
                            </tr>
                          </table>
                        </td>
                      </tr>

                      <!-- Feature 3 -->
                      <tr>
                        <td>
                          <table cellpadding="0" cellspacing="0">
                            <tr>
                              <td style="width:40px;vertical-align:top;padding-top:2px;">
                                <div style="background:#FF6B00;border-radius:50%;width:32px;height:32px;text-align:center;line-height:32px;font-size:15px;">&#127918;</div>
                              </td>
                              <td style="padding-left:14px;">
                                <p style="color:#ffffff;font-size:14px;font-weight:700;margin:0 0 4px;">Reviews &amp; Deep Dives</p>
                                <p style="color:#6b7280;font-size:13px;line-height:1.5;margin:0;">In-depth game reviews, patch notes analysis, and exclusive interviews.</p>
                              </td>
                            </tr>
                          </table>
                        </td>
                      </tr>

                    </table>
                  </td>
                </tr>

              </table>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td align="center" style="padding:24px 0 8px;">
              <p style="color:#4b5563;font-size:12px;margin:0;">GNEWZ &mdash; Gaming &amp; Esports News</p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

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
