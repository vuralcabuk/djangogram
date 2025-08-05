import pytest
from posts.models import SocialShare
from posts.tasks import fake_instagram_share
from users.models import User

@pytest.mark.django_db
def test_fake_instagram_share_task():
    # 1. Test kullanıcı oluştur
    user = User.objects.create_user(username="testuser", password="password")

    # 2. Bir SocialShare nesnesi oluştur
    share = SocialShare.objects.create(
        user=user,
        platform="instagram",
        message="Test paylaşımı",
        status="pending"
    )

    # 3. Görevi doğrudan çalıştır
    fake_instagram_share(share.id, share.message)

    # 4. Veritabanından tekrar al ve durumu kontrol et
    share.refresh_from_db()
    assert share.status == "shared"
