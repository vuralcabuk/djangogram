from django.urls import path
from .api_views import LoginAPI, LogoutAPI, WhoAmI,ProfileAPI

urlpatterns = [
    path('api/login/', LoginAPI.as_view(), name='api-login'),
    path('api/logout/', LogoutAPI.as_view(), name='api-logout'),
    path('api/whoami/', WhoAmI.as_view(), name='api-whoami'),
    path('api/profile/', ProfileAPI.as_view(), name='api-profile'),
]
