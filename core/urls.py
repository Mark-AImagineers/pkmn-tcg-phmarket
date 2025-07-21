from django.urls import path
from .views import HomeView, SettingsView, AdminPanelView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("settings/", SettingsView.as_view(), name="settings"),
    path("settings/admin/", AdminPanelView.as_view(), name="admin_panel"),
]
