from celery import shared_task
import time

@shared_task
def test_gorevi():
    print("⏳ Görev başlatıldı...")
    time.sleep(5)
    print("✅ Görev tamamlandı!")
    return "Bitti"


