from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.urls import reverse
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
import io

class UserTests(APITestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "testpass123"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()

    def test_register_user(self):
        url = reverse('register')
        data = {
            "username": "newuser",
            "password1": "newpass123",
            "password2": "newpass123",
            "email": "newuser@example.com"
        }
        response = self.client.post(url, data)
        self.assertIn(response.status_code, [200, 302])
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_login_api(self):
        url = reverse('api-login')
        data = {"username": self.username, "password": self.password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)

    def test_logout_api(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('api-logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("detail"), "Token deleted, logged out.")

    def test_whoami_api(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('api-whoami')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("username"), self.username)

def test_profile_create_and_retrieve(self):
    self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    url = reverse('api-profile')

    # Profil GET (boş çekme)
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)

    # Geçici dosya oluştur
    tmp_image = tempfile.NamedTemporaryFile(suffix=".jpg")
    tmp_image.write(b"\x47\x49\x46")  # minimal geçerli içerik gibi kabul etmesi için dummy data
    tmp_image.seek(0)

    data = {
        "bio": "Ben test kullanıcısıyım.",
        "profile_image": tmp_image,
    }
    response = self.client.put(url, data, format='multipart')
    print("PUT Response Data:", response.data)  # Debug için

    self.assertIn(response.status_code, [200, 201])

    # Profili tekrar çek
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data.get("bio"), "Ben test kullanıcısıyım.")




    def test_unauthorized_access(self):
        url = reverse('api-whoami')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)  # Token olmadan erişim engellenmeli

    def test_invalid_login(self):
        url = reverse('api-login')
        data = {"username": "wrong", "password": "wrongpass"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 401)
