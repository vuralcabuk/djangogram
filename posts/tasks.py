import time
import logging
import random
from celery import shared_task
from .models import SocialShare
from .constants import SocialShareStatus

logger = logging.getLogger(__name__)

@shared_task
def fake_instagram_share(share_id):
    logger.info(f"[Instagram] Paylaşım başlatıldı (Share ID: {share_id})")

    time.sleep(random.randint(2, 4))  # Simüle gecikme

    try:
        share = SocialShare.objects.get(id=share_id)
        share.status = SocialShareStatus.SHARED.value
        share.save()
        logger.info(f"[Instagram] Paylaşım tamamlandı (Share ID: {share_id}) | Mesaj: {share.message}")
    except SocialShare.DoesNotExist:
        logger.warning(f"[Instagram] Share ID {share_id} bulunamadı")


@shared_task
def fake_facebook_share(share_id):
    logger.info(f"[Facebook] Paylaşım başlatıldı (Share ID: {share_id})")

    time.sleep(random.randint(1, 3))  # Simüle gecikme

    try:
        share = SocialShare.objects.get(id=share_id)
        share.status = SocialShareStatus.SHARED.value
        share.save()
        logger.info(f"[Facebook] Paylaşım tamamlandı (Share ID: {share_id}) | Mesaj: {share.message}")
    except SocialShare.DoesNotExist:
        logger.warning(f"[Facebook] Share ID {share_id} bulunamadı")


@shared_task
def fake_whatsapp_share(share_id):
    logger.info(f"[WhatsApp] Paylaşım başlatıldı (Share ID: {share_id})")

    time.sleep(random.randint(1, 2))  # Simüle gecikme

    try:
        share = SocialShare.objects.get(id=share_id)
        share.status = SocialShareStatus.SHARED.value
        share.save()
        logger.info(f"[WhatsApp] Paylaşım tamamlandı (Share ID: {share_id}) | Mesaj: {share.message}")
    except SocialShare.DoesNotExist:
        logger.warning(f"[WhatsApp] Share ID {share_id} bulunamadı")


@shared_task
def handle_social_share(share_id):
    """
    Verilen SocialShare ID'sine göre platformu kontrol eder
    ve ilgili paylaşım görevini Celery'e gönderir.
    """
    try:
        share = SocialShare.objects.get(id=share_id)
        platform = share.platform

        if platform == "instagram":
            fake_instagram_share.delay(share_id)
        elif platform == "facebook":
            fake_facebook_share.delay(share_id)
        elif platform == "whatsapp":
            fake_whatsapp_share.delay(share_id)
        else:
            logger.warning(f"[UNKNOWN PLATFORM] Tanımsız platform: {platform}")
    except SocialShare.DoesNotExist:
        logger.error(f"[SHARE NOT FOUND] SocialShare id {share_id} bulunamadı")
