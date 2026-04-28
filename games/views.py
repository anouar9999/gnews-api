from django.db.models import Max
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Game
from .serializers import GameSerializer
from accounts.permissions import IsAdminOrEditorOrReadOnly


class GameViewSet(viewsets.ModelViewSet):
    serializer_class = GameSerializer
    permission_classes = [IsAdminOrEditorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['game_type', 'is_active']
    search_fields = ['title', 'genre', 'developer', 'publisher']
    ordering_fields = ['rank', 'title', 'created_at', 'hype_score', 'popularity_score']
    ordering = ['rank']
    lookup_field = 'slug'

    def get_queryset(self):
        qs = Game.objects.prefetch_related('categories')
        if self.request.user.is_authenticated:
            return qs
        return qs.filter(is_active=True)

    def perform_create(self, serializer):
        rank = serializer.validated_data.get('rank', 0)
        if not rank:
            max_rank = Game.objects.aggregate(m=Max('rank'))['m'] or 0
            serializer.save(rank=max_rank + 1)
        else:
            serializer.save()
