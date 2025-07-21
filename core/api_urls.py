from django.urls import path

from .api_views import SendTestEmailAPIView

urlpatterns = [
    path("test-email/", SendTestEmailAPIView.as_view(), name="api_test_email"),
]
