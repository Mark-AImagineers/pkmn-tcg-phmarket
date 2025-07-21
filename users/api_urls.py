from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .api_views import MeAPIView, RegistrationAPIView

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="api_login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="api_token_refeesh"),
    path("register/", RegistrationAPIView.as_view(), name="api_register"),
    path("me/", MeAPIView.as_view(), name="api_me"),
]
