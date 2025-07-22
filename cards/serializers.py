"""Serializers for the cards app."""

from rest_framework import serializers

from .models import Attack, Card, CardSet, TCGPlayerPrice, Weakness


class CardSetSerializer(serializers.ModelSerializer):
    """Serializer for ``CardSet`` objects."""

    class Meta:
        model = CardSet
        fields = [
            "id",
            "set_id",
            "name",
            "series",
            "printed_total",
            "total",
            "ptcgo_code",
            "release_date",
            "updated_at",
            "symbol_image",
            "logo_image",
        ]


class AttackSerializer(serializers.ModelSerializer):
    """Serializer for ``Attack`` objects."""

    class Meta:
        model = Attack
        fields = [
            "id",
            "name",
            "cost",
            "converted_energy_cost",
            "damage",
            "text",
        ]


class WeaknessSerializer(serializers.ModelSerializer):
    """Serializer for ``Weakness`` objects."""

    class Meta:
        model = Weakness
        fields = ["id", "type", "value"]


class TCGPlayerPriceSerializer(serializers.ModelSerializer):
    """Serializer for ``TCGPlayerPrice`` objects."""

    class Meta:
        model = TCGPlayerPrice
        fields = [
            "url",
            "updated_at",
            "low",
            "mid",
            "high",
            "market",
            "direct_low",
        ]


class CardSerializer(serializers.ModelSerializer):
    """Serializer for ``Card`` objects with nested relations."""

    attacks = AttackSerializer(many=True, read_only=True)
    weaknesses = WeaknessSerializer(many=True, read_only=True)
    tcgplayer_price = TCGPlayerPriceSerializer(read_only=True)
    set = CardSetSerializer(read_only=True)

    class Meta:
        model = Card
        fields = [
            "id",
            "card_id",
            "name",
            "supertype",
            "subtypes",
            "hp",
            "types",
            "evolves_to",
            "rules",
            "retreat_cost",
            "converted_retreat_cost",
            "number",
            "artist",
            "rarity",
            "national_pokedex_numbers",
            "small_image",
            "large_image",
            "set",
            "attacks",
            "weaknesses",
            "tcgplayer_price",
        ]
