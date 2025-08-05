import pytest
from posts.models import SocialShare
from posts.tasks import fake_instagram_share
from users.models import User
from posts.constants import SocialShareStatus


@pytest.mark.django_db
def test_fake_instagram_share_task_with_celery():
    # 1. Kullanıcı oluştur
    user = User.objects.create_user(username="testuser", password="password")

    # 2. SocialShare nesnesi oluştur
    share = SocialShare.objects.create(
        user=user,
        platform="instagram",
        message="Test paylaşımı",
        status="pending"
    )

    # 3. Görevi Celery kuyruğuna gönder
    result = fake_instagram_share.delay(share.id, share.message)

    # 4. Sonucu bekle (Celery + Redis çalışıyor olmalı)
    output = result.get(timeout=10)

    # 5. Güncellenmiş nesneyi al
    share.refresh_from_db()

    # 6. Kontroller
    assert share.status == "completed"
    assert output == "Instagram paylaşımı tamamlandı"

def test_fake_instagram_share():
    ...
    assert updated_share.status == SocialShareStatus.SHARED.value, f"Beklenen status: {SocialShareStatus.SHARED.value}, fakat gelen: {updated_share.status}"

