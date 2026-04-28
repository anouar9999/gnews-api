from rest_framework import serializers
from .models import Article, Category, Tag, Source, Media, RawNews, NewsletterSubscriber, Comment, SitePage, SiteSettings, LandingSection, LandingSectionArticle


class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'type', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ['id', 'name', 'type', 'url', 'fetch_interval', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'url', 'alt_text', 'caption', 'credit', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class RawNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawNews
        fields = ['id', 'source', 'title', 'url', 'content', 'status', 'raw_data', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ArticleListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'meta_description',
            'featured_image', 'featured_image_b64', 'status',
            'is_featured', 'is_breaking', 'view_count',
            'category', 'tags',
            'published_at', 'created_at', 'updated_at'
        ]


class ArticleDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    source = SourceSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    media = MediaSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'content',
            'meta_title', 'meta_description',
            'featured_image', 'featured_image_b64',
            'status', 'is_featured', 'is_breaking', 'view_count',
            'validation_notes',
            'source', 'raw_news', 'category',
            'tags', 'media',
            'published_at', 'created_at', 'updated_at'
        ]


class ArticleCreateUpdateSerializer(serializers.ModelSerializer):
    tag_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    media_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    featured_image = serializers.ImageField(required=False, allow_null=True, allow_empty_file=True)

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'content',
            'meta_title', 'meta_description',
            'featured_image', 'featured_image_b64',
            'status', 'is_featured', 'is_breaking',
            'validation_notes',
            'source', 'raw_news', 'category',
            'tag_ids', 'media_ids',
            'published_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        tag_ids = validated_data.pop('tag_ids', [])
        media_ids = validated_data.pop('media_ids', [])

        article = Article.objects.create(**validated_data)

        if tag_ids:
            article.tags.set(tag_ids)
        if media_ids:
            article.media.set(media_ids)

        return article

    def update(self, instance, validated_data):
        tag_ids = validated_data.pop('tag_ids', None)
        media_ids = validated_data.pop('media_ids', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tag_ids is not None:
            instance.tags.set(tag_ids)
        if media_ids is not None:
            instance.media.set(media_ids)

        return instance


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = ['general', 'content_cfg', 'updated_at']
        read_only_fields = ['updated_at']


class SitePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SitePage
        fields = ['slug', 'content', 'updated_at']
        read_only_fields = ['updated_at']


class LandingSectionArticleSerializer(serializers.ModelSerializer):
    article = ArticleListSerializer(read_only=True)

    class Meta:
        model = LandingSectionArticle
        fields = ['id', 'article', 'position']


class LandingSectionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True, allow_null=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True, allow_null=True)
    articles      = LandingSectionArticleSerializer(source='section_articles', many=True, read_only=True)
    article_ids   = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
    )

    class Meta:
        model  = LandingSection
        fields = [
            'id', 'key', 'label', 'category', 'category_name', 'category_slug',
            'article_count', 'is_active',
            'articles', 'article_ids',
            'updated_at',
        ]
        read_only_fields = ['id', 'updated_at']

    def update(self, instance, validated_data):
        article_ids = validated_data.pop('article_ids', None)
        instance = super().update(instance, validated_data)
        if article_ids is not None:
            LandingSectionArticle.objects.filter(section=instance).delete()
            for i, aid in enumerate(article_ids):
                LandingSectionArticle.objects.create(section=instance, article_id=aid, position=i)
        return instance


class CommentReplySerializer(serializers.ModelSerializer):
    """Shallow serializer for replies (no further nesting)."""
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'author_name', 'author_email', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_author_name(self, obj):
        if obj.author:
            return obj.author.get_full_name() or obj.author.username
        return obj.author_name or 'Anonymous'


class CommentSerializer(serializers.ModelSerializer):
    """Top-level comment with nested replies."""
    replies = CommentReplySerializer(many=True, read_only=True)
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'article', 'parent',
            'author_name', 'author_email',
            'content', 'replies',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'article', 'created_at', 'updated_at']

    def get_author_name(self, obj):
        if obj.author:
            return obj.author.get_full_name() or obj.author.username
        return obj.author_name or 'Anonymous'


class CommentCreateSerializer(serializers.ModelSerializer):
    """Used for POST — clients supply content, optional name/email/parent."""

    class Meta:
        model = Comment
        fields = ['parent', 'author_name', 'author_email', 'content']

    def validate_parent(self, value):
        if value and value.parent is not None:
            raise serializers.ValidationError('Replies cannot be nested more than one level.')
        return value
