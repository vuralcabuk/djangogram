from django.urls import path
from .views import SocialShareCreateView, SocialShareListView

urlpatterns = [
    path('share/', SocialShareCreateView.as_view(), name='social-share'),
    path('shares/', SocialShareListView.as_view(), name='social_share_list'),
]
