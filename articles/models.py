from django.db import models
from django.utils.text import slugify


class Source(models.Model):
    TYPE_CHOICES = [
        ('rss', 'RSS'),
        ('api', 'API'),
        ('scraper', 'Scraper'),
    ]
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    url = models.TextField()
    fetch_interval = models.PositiveIntegerField(default=30)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sources'

    def __str__(self):
        return self.name


class RawNews(models.Model):
    STATUS_CHOICES = [
        ('nouveau', 'Nouveau'),
        ('traite', 'Traite'),
        ('ignore', 'Ignore'),
    ]
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True, related_name='raw_news')
    title = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='nouveau')
    raw_data = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'raw_news'
        verbose_name_plural = 'Raw news'

    def __str__(self):
        return self.title or f'RawNews #{self.pk}'


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    TYPE_CHOICES = [
        ('game', 'Game'),
        ('platform', 'Platform'),
        ('genre', 'Genre'),
        ('general', 'General'),
    ]
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='general')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tags'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Media(models.Model):
    url = models.TextField()
    alt_text = models.CharField(max_length=500, blank=True, null=True)
    caption = models.TextField(blank=True, null=True)
    credit = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'media'
        verbose_name_plural = 'Media'

    def __str__(self):
        return self.url[:50]


class Article(models.Model):
    STATUS_CHOICES = [
        ('nouveau', 'Nouveau'),
        ('brouillon_ia', 'Brouillon IA'),
        ('en_revision', 'En Revision'),
        ('publie', 'Publie'),
        ('archive', 'Archive'),
    ]

    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles')
    raw_news = models.ForeignKey(RawNews, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles')

    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500, unique=True)
    content = models.TextField()

    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)

    featured_image = models.ImageField(upload_to='articles/featured/', blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='nouveau')

    is_featured = models.BooleanField(default=False)
    is_breaking = models.BooleanField(default=False)

    view_count = models.PositiveBigIntegerField(default=0)

    validation_notes = models.TextField(blank=True, null=True)

    tags = models.ManyToManyField(Tag, through='ArticleTag', related_name='articles')
    media = models.ManyToManyField(Media, through='ArticleMedia', related_name='articles')

    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'articles'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ArticleMedia(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    order_position = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'article_media'
        unique_together = ('article', 'media')
        ordering = ['order_position']


class ArticleTag(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'article_tags'
        unique_together = ('article', 'tag')


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'newsletter_subscribers'

    def __str__(self):
        return self.email
