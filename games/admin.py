from django.contrib import admin
from .models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['title', 'game_type', 'genre', 'rank', 'is_active', 'created_at']
    list_filter = ['game_type', 'is_active', 'genre', 'status']
    search_fields = ['title', 'developer', 'publisher']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['rank']
    filter_horizontal = ['categories']
