from rest_framework import serializers
from .models import Post, Media, SocialShare

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'media_type', 'file', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    media = MediaSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'created_at', 'media', 'share_status']

class SocialShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialShare
        fields = ['id', 'platform', 'message', 'media', 'status', 'created_at', 'updated_at']
        read_only_fields = ['status', 'created_at', 'updated_at']
