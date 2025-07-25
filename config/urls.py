from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),  # homepage and other common pages
    path("api/", include("users.api_urls")),  # for DRF API endpoints like /api/login/
    path("api/", include("core.api_urls")),
    path("api/", include("cards.api_urls")),
    path("", include("cards.urls")),
    path("", include("users.urls")),  # for HTMX views like /login/
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
