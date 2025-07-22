from django.views.generic import TemplateView


class ManageGlobalCardsView(TemplateView):
    """Admin page for managing global card data."""

    template_name = "cards/manage_global_cards.html"
