from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('viewer', 'Viewer'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='viewer')

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username
