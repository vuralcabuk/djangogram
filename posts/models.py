from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .constants import SocialShareStatus


User = get_user_model()


def validate_file_type(file):
    import os
    ext = os.path.splitext(file.name)[1].lower()
    valid_image_extensions = ['.jpg', '.jpeg', '.png']
    valid_video_extensions = ['.mp4', '.mov', '.avi']
    if ext not in valid_image_extensions + valid_video_extensions:
        raise ValidationError('Sadece görsel (.jpg, .png) veya video (.mp4, .mov) yüklenebilir.')


class SocialShare(models.Model):
    PLATFORM_CHOICES = [
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('whatsapp', 'WhatsApp'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_shares')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    message = models.TextField(blank=True) # mesaj boş olabilir
    status = models.CharField(
        max_length=20,
        choices=[(status.value, status.name) for status in SocialShareStatus],
        default=SocialShareStatus.PENDING.value
    )
    media = models.FileField(upload_to='social_shares/media/', blank=True, null=True, validators=[validate_file_type])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.platform} - {self.status}"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(blank=True)
    #media = models.FileField(upload_to='posts/media/', validators=[validate_file_type], blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    share_status = models.CharField(max_length=20,choices=[(status.value, status.value) for status in SocialShareStatus],default=SocialShareStatus.PENDING.value,)

class Media(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="media_items")
    file = models.FileField(upload_to='media/')
    media_type = models.CharField(max_length=10, choices=(('image', 'Image'), ('video', 'Video')))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.media_type} for {self.post}"
