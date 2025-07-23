from celery import shared_task
from .models import SocialShare
import time, random

@shared_task
def share_post_task(social_share_id):
    try:
        share = SocialShare.objects.get(id=social_share_id)
        # Sahte paylaşım işlemi
        share.status = "shared"
        share.save()
    except SocialShare.DoesNotExist:
        pass

@shared_task
def fake_instagram_share(post_id, caption):
    from .models import SocialShare  # İçeride import edelim, Celery'de bazen dışarıdan import sorun çıkarabiliyor
    print(f"Instagram'a gönderi ({post_id}) paylaşımı başlatıldı...")

    # Simüle bir gecikme (mesela API'ye istek atıyormuşuz gibi)
    time.sleep(random.randint(2,5))

    print(f"Instagram'a gönderi ({post_id}) paylaşıldı. Yazı: {caption}")

    try:
        share = SocialShare.objects.get(id=post_id)
        share.status = "shared"
        share.save()
    except SocialShare.DoesNotExist:
        print(f"SocialShare id={post_id} bulunamadı.")

    return f"Paylaşım ({post_id}) tamamlandı."

