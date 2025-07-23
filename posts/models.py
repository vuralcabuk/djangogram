from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class SocialShare(models.Model):
    PLATFORM_CHOICES = [
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('whatsapp', 'WhatsApp'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Beklemede'),
        ('in_progress', 'Gönderiliyor'),
        ('success', 'Başarılı'),
        ('failed', 'Hata'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_shares')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.platform} - {self.status}"
