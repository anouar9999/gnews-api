from rest_framework import serializers
from .models import Game
from articles.models import Category


class CategoryMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class GameSerializer(serializers.ModelSerializer):
    categories = CategoryMiniSerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all(),
        source='categories',
        write_only=True,
        required=False,
    )
    release_date = serializers.DateField(allow_null=True, required=False)
    metacritic = serializers.IntegerField(allow_null=True, required=False, min_value=0, max_value=100)
    rating = serializers.FloatField(allow_null=True, required=False, min_value=0, max_value=5)

    class Meta:
        model = Game
        fields = [
            'id', 'title', 'slug', 'description', 'short_description',
            'cover_image', 'trailer_url', 'genre', 'platforms',
            'developer', 'publisher', 'release_date', 'release_display',
            'game_type', 'status', 'hype_score', 'popularity_score',
            'player_count', 'metacritic', 'rating', 'rank', 'trend',
            'is_active', 'categories', 'category_ids', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
