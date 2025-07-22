from django.urls import path

from .views import ManageGlobalCardsView


urlpatterns = [
    path(
        "settings/admin/cards/",
        ManageGlobalCardsView.as_view(),
        name="manage_global_cards",
    ),
]
