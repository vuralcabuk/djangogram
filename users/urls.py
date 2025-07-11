from django.urls import path
from .api_views import (
    LoginAPI, LogoutAPI, WhoAmI, ProfileAPI,
    PostCreateAPI, PostListAPI, UsersPostAPI
)

urlpatterns = [
    # Auth işlemleri
    path('api/login/', LoginAPI.as_view(), name='api-login'),
    path('api/logout/', LogoutAPI.as_view(), name='api-logout'),
    path('api/whoami/', WhoAmI.as_view(), name='api-whoami'),

    # Profil
    path('api/profile/', ProfileAPI.as_view(), name='api-profile'),

    # Gönderiler
    path('api/posts/', PostCreateAPI.as_view(), name='api-post-create'),      # POST gönderi oluştur
    path('api/posts/all/', PostListAPI.as_view(), name='api-post-list'),      # GET tüm gönderiler
    path('api/posts/me/', UsersPostAPI.as_view(), name='api-user-posts'),     # GET kendi gönderileri
]
