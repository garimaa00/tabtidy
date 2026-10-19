from django.conf import settings
from django.db import models


class SavedLink(models.Model):
    CATEGORY_CHOICES = [
        ('Coding', 'Coding'),
        ('Learning', 'Learning'),
        ('Jobs', 'Jobs'),
        ('Design', 'Design'),
        ('Personal', 'Personal'),
        ('Other', 'Other'),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='saved_links',
        null=True,
        blank=True,
    )

    title = models.CharField(max_length=150)
    url = models.URLField(max_length=500)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='Other',
    )
    note = models.TextField(blank=True)
    is_visited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_favourite = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_pinned', 'is_visited', '-created_at']

    def __str__(self):
        return self.title

