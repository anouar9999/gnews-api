from rest_framework import serializers
from .models import Article, Category, Tag, Source, Media, RawNews, NewsletterSubscriber


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
            'id', 'title', 'slug', 'featured_image', 'status',
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
            'meta_title', 'meta_description', 'featured_image',
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
            'meta_title', 'meta_description', 'featured_image',
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
