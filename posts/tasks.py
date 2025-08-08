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
        # Fake medya içeriği varsa bunu loglayalım
        media_info = f" | Medya: {share.media.url}" if share.media else ""
        logger.info(f"[Instagram] Paylaşım tamamlandı (Share ID: {share_id}) | Mesaj: {share.message}{media_info}")
        share.status = SocialShareStatus.SHARED.value
        share.save()
    except SocialShare.DoesNotExist:
        logger.warning(f"[Instagram] Share ID {share_id} bulunamadı")
    except Exception as e:
        logger.error(f"[Instagram] Hata: {str(e)}")
        if 'share' in locals():
            share.status = SocialShareStatus.FAILED.value
            share.save()

@shared_task
def fake_facebook_share(share_id):
    logger.info(f"[Facebook] Paylaşım başlatıldı (Share ID: {share_id})")

    time.sleep(random.randint(1, 3))  # Simüle gecikme

    try:
        share = SocialShare.objects.get(id=share_id)
        media_info = f" | Medya: {share.media.url}" if share.media else ""
        logger.info(f"[Facebook] Paylaşım tamamlandı (Share ID: {share_id}) | Mesaj: {share.message}{media_info}")
        share.status = SocialShareStatus.SHARED.value
        share.save()
    except SocialShare.DoesNotExist:
        logger.warning(f"[Facebook] Share ID {share_id} bulunamadı")
    except Exception as e:
        logger.error(f"[Facebook] Hata: {str(e)}")
        if 'share' in locals():
            share.status = SocialShareStatus.FAILED.value
            share.save()

@shared_task
def fake_whatsapp_share(share_id):
    logger.info(f"[WhatsApp] Paylaşım başlatıldı (Share ID: {share_id})")

    time.sleep(random.randint(1, 2))  # Simüle gecikme

    try:
        share = SocialShare.objects.get(id=share_id)
        media_info = f" | Medya: {share.media.url}" if share.media else ""
        logger.info(f"[WhatsApp] Paylaşım tamamlandı (Share ID: {share_id}) | Mesaj: {share.message}{media_info}")
        share.status = SocialShareStatus.SHARED.value
        share.save()
    except SocialShare.DoesNotExist:
        logger.warning(f"[WhatsApp] Share ID {share_id} bulunamadı")
    except Exception as e:
        logger.error(f"[WhatsApp] Hata: {str(e)}")
        if 'share' in locals():
            share.status = SocialShareStatus.FAILED.value
            share.save()

@shared_task
def handle_social_share(share_id):
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
            share.status = SocialShareStatus.FAILED.value
            share.save()
    except SocialShare.DoesNotExist:
        logger.error(f"[SHARE NOT FOUND] SocialShare id {share_id} bulunamadı")
