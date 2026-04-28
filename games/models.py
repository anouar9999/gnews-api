from django.db import models
from django.utils.text import slugify


class Game(models.Model):
    GAME_TYPE_CHOICES = [
        ('popular', 'Popular'),
        ('anticipated', 'Anticipated'),
        ('both', 'Both'),
    ]
    STATUS_CHOICES = [
        ('coming_soon', 'Coming Soon'),
        ('tba', 'TBA'),
        ('released', 'Released'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True)
    short_description = models.CharField(max_length=500, blank=True)
    cover_image = models.URLField(max_length=2000, blank=True)
    trailer_url = models.URLField(max_length=2000, blank=True)
    genre = models.CharField(max_length=100, blank=True)
    platforms = models.JSONField(default=list)
    developer = models.CharField(max_length=200, blank=True)
    publisher = models.CharField(max_length=200, blank=True)
    release_date = models.DateField(null=True, blank=True)
    release_display = models.CharField(max_length=50, blank=True, default='TBA')
    game_type = models.CharField(max_length=20, choices=GAME_TYPE_CHOICES, default='popular')
    # Anticipated-specific
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='coming_soon', blank=True)
    hype_score = models.IntegerField(default=80)
    # Popular-specific
    popularity_score = models.IntegerField(default=75)
    player_count = models.CharField(max_length=50, blank=True)
    metacritic = models.IntegerField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    # Shared
    rank = models.IntegerField(default=0, db_index=True)
    trend = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    categories = models.ManyToManyField('articles.Category', blank=True, related_name='games')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'games'
        ordering = ['rank', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug = base
            n = 1
            while Game.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)
