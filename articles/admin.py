from django.contrib import admin
from .models import Source, RawNews, Category, Tag, Media, Article, ArticleMedia, ArticleTag


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'is_active', 'fetch_interval', 'created_at']
    list_filter = ['type', 'is_active']
    search_fields = ['name', 'url']


@admin.register(RawNews)
class RawNewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'source', 'status', 'created_at']
    list_filter = ['status', 'source']
    search_fields = ['title', 'content']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'created_at']
    list_filter = ['parent']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'type', 'created_at']
    list_filter = ['type']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ['id', 'alt_text', 'created_at']
    search_fields = ['alt_text', 'caption', 'credit']


class ArticleMediaInline(admin.TabularInline):
    model = ArticleMedia
    extra = 1


class ArticleTagInline(admin.TabularInline):
    model = ArticleTag
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'category', 'is_featured', 'is_breaking', 'view_count', 'published_at']
    list_filter = ['status', 'is_featured', 'is_breaking', 'category']
    search_fields = ['title', 'content', 'meta_title', 'meta_description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ArticleTagInline, ArticleMediaInline]
    date_hierarchy = 'created_at'
    raw_id_fields = ['source', 'raw_news']
