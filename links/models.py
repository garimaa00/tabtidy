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

    class Meta:
        ordering = ['is_visited', '-created_at']

    def __str__(self):
        return self.title

