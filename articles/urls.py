from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ArticleViewSet, CategoryViewSet, TagViewSet, SourceViewSet,
    MediaViewSet, RawNewsViewSet, NewsletterSubscribeView, SendEmailView,
    GlobalStatsView, ArticleStatsView, SourceStatsView, RawNewsStatsView,
    CategoryStatsView, TagStatsView, NewsletterStatsView, UserStatsView,
    ArticleCommentListCreateView, ArticleCommentDetailView,
    SitePageViewSet, SiteSettingsView, LandingSectionViewSet,
)

router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'sources', SourceViewSet, basename='source')
router.register(r'media', MediaViewSet, basename='media')
router.register(r'raw-news', RawNewsViewSet, basename='raw-news')
router.register(r'pages', SitePageViewSet, basename='site-page')
router.register(r'landing-sections', LandingSectionViewSet, basename='landing-section')

urlpatterns = [
    path('', include(router.urls)),
    path('settings/', SiteSettingsView.as_view(), name='site-settings'),
    path('newsletter/subscribe/', NewsletterSubscribeView.as_view(), name='newsletter-subscribe'),
    path('email/send/', SendEmailView.as_view(), name='email-send'),
    # Statistics
    path('stats/', GlobalStatsView.as_view(), name='stats-global'),
    path('stats/articles/', ArticleStatsView.as_view(), name='stats-articles'),
    path('stats/sources/', SourceStatsView.as_view(), name='stats-sources'),
    path('stats/raw-news/', RawNewsStatsView.as_view(), name='stats-raw-news'),
    path('stats/categories/', CategoryStatsView.as_view(), name='stats-categories'),
    path('stats/tags/', TagStatsView.as_view(), name='stats-tags'),
    path('stats/newsletter/', NewsletterStatsView.as_view(), name='stats-newsletter'),
    path('stats/users/', UserStatsView.as_view(), name='stats-users'),
    # Comments
    path('articles/<int:article_id>/comments/', ArticleCommentListCreateView.as_view(), name='article-comments'),
    path('articles/<int:article_id>/comments/<int:comment_id>/', ArticleCommentDetailView.as_view(), name='article-comment-detail'),
]
