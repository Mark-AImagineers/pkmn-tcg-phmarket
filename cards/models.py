from django.db import models


class CardSet(models.Model):
    """A trading card game set."""

    set_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    series = models.CharField(max_length=100)
    printed_total = models.IntegerField()
    total = models.IntegerField()
    ptcgo_code = models.CharField(max_length=20, null=True, blank=True)
    release_date = models.DateField()
    updated_at = models.DateTimeField()
    symbol_image = models.URLField()
    logo_image = models.URLField()

    def __str__(self) -> str:
        return self.name


class Card(models.Model):
    """An individual trading card."""

    card_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    supertype = models.CharField(max_length=50)
    subtypes = models.JSONField(null=True, blank=True)
    hp = models.CharField(max_length=10, null=True, blank=True)
    types = models.JSONField(null=True, blank=True)
    evolves_to = models.JSONField(null=True, blank=True)
    rules = models.JSONField(null=True, blank=True)
    retreat_cost = models.JSONField(null=True, blank=True)
    converted_retreat_cost = models.IntegerField(null=True, blank=True)
    number = models.CharField(max_length=10)
    artist = models.CharField(max_length=100, null=True, blank=True)
    rarity = models.CharField(max_length=50, null=True, blank=True)
    national_pokedex_numbers = models.JSONField(null=True, blank=True)
    small_image = models.URLField(null=True, blank=True)
    large_image = models.URLField(null=True, blank=True)
    set = models.ForeignKey(CardSet, on_delete=models.CASCADE, related_name="cards")

    def __str__(self) -> str:
        return self.name


class Attack(models.Model):
    """An attack that a card can perform."""

    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="attacks")
    name = models.CharField(max_length=100)
    cost = models.JSONField(null=True, blank=True)
    converted_energy_cost = models.IntegerField()
    damage = models.CharField(max_length=20)
    text = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.card.name} - {self.name}"


class Weakness(models.Model):
    """A weakness of a card."""

    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="weaknesses")
    type = models.CharField(max_length=50)
    value = models.CharField(max_length=10)

    def __str__(self) -> str:
        return f"{self.card.name} weakness to {self.type}"


class TCGPlayerPrice(models.Model):
    """Pricing information for a card from TCGPlayer."""

    card = models.OneToOneField(
        Card, on_delete=models.CASCADE, related_name="tcgplayer_price"
    )
    url = models.URLField()
    updated_at = models.DateField()
    low = models.FloatField(null=True, blank=True)
    mid = models.FloatField(null=True, blank=True)
    high = models.FloatField(null=True, blank=True)
    market = models.FloatField(null=True, blank=True)
    direct_low = models.FloatField(null=True, blank=True)

    def __str__(self) -> str:
        return f"Prices for {self.card.name}"
