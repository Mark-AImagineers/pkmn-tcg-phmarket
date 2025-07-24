from django.contrib import admin
from .models import CardRef, Card, CardSet, Attack, Weakness

admin.site.register(CardRef)
admin.site.register(Card)
admin.site.register(CardSet)
admin.site.register(Attack)
admin.site.register(Weakness)