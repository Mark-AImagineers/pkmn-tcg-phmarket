from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView


class HomeView(LoginRequiredMixin, TemplateView):
    """Basic homepage for authenticated users."""

    template_name = "core/home.html"


class SettingsView(LoginRequiredMixin, TemplateView):
    """Display settings available to the authenticated user."""

    template_name = "core/settings.html"


class AdminPanelView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """Simple admin panel accessible only to superusers."""

    template_name = "core/admin_panel.html"

    def test_func(self) -> bool:
        return bool(self.request.user and self.request.user.is_superuser)
