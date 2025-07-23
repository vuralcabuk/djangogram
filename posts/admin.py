from django.contrib import admin
from .models import SocialShare

@admin.register(SocialShare)
class SocialShareAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'platform', 'status', 'created_at')
    list_filter = ('platform', 'status')
    search_fields = ('user_username', 'message')

