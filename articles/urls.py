from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, CategoryViewSet, TagViewSet, SourceViewSet, MediaViewSet, RawNewsViewSet

router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'sources', SourceViewSet, basename='source')
router.register(r'media', MediaViewSet, basename='media')
router.register(r'raw-news', RawNewsViewSet, basename='raw-news')

urlpatterns = [
    path('', include(router.urls)),
]
