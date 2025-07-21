from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Basic homepage for authenticated users."""

    template_name = "core/home.html"


class SettingsView(TemplateView):
    """Display settings available to the authenticated user."""

    template_name = "core/settings.html"


class AdminPanelView(TemplateView):
    """Simple admin panel for superusers. Visibility controlled client-side."""

    template_name = "core/admin_panel.html"
