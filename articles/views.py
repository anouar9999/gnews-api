from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings as django_settings

from .models import Article, Category, Tag, Source, Media, RawNews, NewsletterSubscriber
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
)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.select_related(
        'category', 'source'
    ).prefetch_related('tags', 'media')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'is_featured', 'is_breaking', 'category']
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
            send_mail(
                subject=f'[GNEWZ] {article.title}',
                message=(
                    f'{article.title}\n\n'
                    f'{excerpt}...\n\n'
                    f'Read more: {frontend_url}\n\n'
                    f'---\nUnsubscribe: {frontend_url}'
                ),
                from_email=django_settings.DEFAULT_FROM_EMAIL,
                recipient_list=subscribers,
                fail_silently=True,
            )
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
