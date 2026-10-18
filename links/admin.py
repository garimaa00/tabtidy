from django.contrib import admin
from .models import SavedLink


@admin.register(SavedLink)
class SavedLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_visited', 'created_at')
    list_filter = ('category', 'is_visited')
    search_fields = ('title', 'url')