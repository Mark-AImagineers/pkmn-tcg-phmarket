from django.urls import path

from .api_views import (
    CookieTokenObtainPairView,
    CookieTokenRefreshView,
    LogoutAPIView,
    MeAPIView,
    RegistrationAPIView,
)

urlpatterns = [
    path("login/", CookieTokenObtainPairView.as_view(), name="api_login"),
    path(
        "token/refresh/",
        CookieTokenRefreshView.as_view(),
        name="api_token_refeesh",
    ),
    path("logout/", LogoutAPIView.as_view(), name="api_logout"),
    path("register/", RegistrationAPIView.as_view(), name="api_register"),
    path("me/", MeAPIView.as_view(), name="api_me"),
]
