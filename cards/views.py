from django.views.generic import TemplateView

from .models import Card


class ManageGlobalCardsView(TemplateView):
    """Admin page for managing global card data."""

    template_name = "cards/manage_global_cards.html"

    def get_context_data(self, **kwargs):
        """Return context with all cards for display."""

        context = super().get_context_data(**kwargs)
        context["cards"] = Card.objects.select_related("set").order_by(
            "set__name", "number"
        )
        return context
