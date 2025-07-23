"""Services for syncing card data with the PokéTCG API."""

from __future__ import annotations

import os
import logging
from math import ceil
from typing import Any, List, Optional
from datetime import date, datetime

import requests
from dotenv import load_dotenv
from django.db import transaction

from cards.models import Attack, Card, CardSet, TCGPlayerPrice, Weakness

load_dotenv()

POKETCG_API = os.getenv("POKETCG_API", "")
API_BASE = "https://api.pokemontcg.io/v2"
HEADERS = {"X-Api-Key": POKETCG_API} if POKETCG_API else {}

logger = logging.getLogger(__name__)


def _parse_date(value: str | None) -> Optional[date]:
    """Return a ``date`` object from the API string value."""

    if not value:
        return None
    value = value.replace("/", "-")
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _parse_datetime(value: str | None) -> Optional[datetime]:
    """Return a ``datetime`` object from the API string value."""

    if not value:
        return None
    value = value.replace("/", "-").replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        try:
            return datetime.combine(
                date.fromisoformat(value), datetime.min.time()
            )
        except ValueError:
            return None


def get_all_card_ids() -> List[str]:
    """Return all card IDs from the PokéTCG API.

    The API sometimes returns a 404 or empty page before the reported
    ``totalCount`` is reached. Stop fetching when a page contains no data
    or when the request results in a 404 to avoid unnecessary errors.
    """

    ids: List[str] = []
    page_size = 250
    page = 1
    while True:
        url = f"{API_BASE}/cards?page={page}&pageSize={page_size}"
        try:
            res = requests.get(url, headers=HEADERS, timeout=30)
            if res.status_code == 404:
                break
            res.raise_for_status()
        except requests.HTTPError as exc:  # type: ignore[attr-defined]
            if exc.response is not None and exc.response.status_code == 404:
                break
            raise
        data = res.json()
        records = data.get("data", [])
        if not records:
            break
        ids.extend(card["id"] for card in records)
        total = int(data.get("totalCount", 0))
        if page * page_size >= total:
            break
        page += 1
    return ids


def fetch_card_details(card_id: str) -> dict[str, Any]:
    """Return card details for a given card id.

    Whitespace is stripped from the provided ``card_id``. ``404`` responses
    are handled gracefully and return an empty dictionary.
    """

    clean_id = card_id.strip()
    url = f"{API_BASE}/cards/{clean_id}"
    try:
        res = requests.get(url, headers=HEADERS, timeout=30)
        if res.status_code == 404:
            return {}
        res.raise_for_status()
    except requests.HTTPError as exc:  # type: ignore[attr-defined]
        if exc.response is not None and exc.response.status_code == 404:
            return {}
        raise
    return res.json().get("data", {})


@transaction.atomic
def sync_cards() -> int:
    """Sync missing cards from PokéTCG. Returns number of cards created."""

    ids = get_all_card_ids()
    existing = set(Card.objects.values_list("card_id", flat=True))
    missing = [cid for cid in ids if cid not in existing]
    created = 0
    missing_ids: List[str] = []
    for cid in missing:
        data = fetch_card_details(cid)
        if not data:
            missing_ids.append(cid)
            continue
        card_set = _update_set(data.get("set", {}))
        card = _update_card(data, card_set)
        _update_attacks(card, data.get("attacks", []))
        _update_weaknesses(card, data.get("weaknesses", []))
        _update_tcgplayer(card, data.get("tcgplayer", {}))
        created += 1
    if missing_ids:
        logger.warning("Missing card IDs: %s", ", ".join(missing_ids))
    return created


def _update_set(data: dict[str, Any]) -> CardSet:
    """Create or update a CardSet from API data."""

    defaults = {
        "name": data.get("name", ""),
        "series": data.get("series", ""),
        "printed_total": data.get("printedTotal", 0),
        "total": data.get("total", 0),
        "ptcgo_code": data.get("ptcgoCode"),
        "release_date": _parse_date(data.get("releaseDate")),
        "updated_at": _parse_datetime(data.get("updatedAt")),
        "symbol_image": data.get("images", {}).get("symbol", ""),
        "logo_image": data.get("images", {}).get("logo", ""),
    }
    obj, _ = CardSet.objects.update_or_create(
        set_id=data.get("id"), defaults=defaults
    )
    return obj


def _update_card(data: dict[str, Any], card_set: CardSet) -> Card:
    """Create or update a Card from API data."""

    defaults = {
        "name": data.get("name", ""),
        "supertype": data.get("supertype", ""),
        "subtypes": data.get("subtypes"),
        "hp": data.get("hp"),
        "types": data.get("types"),
        "evolves_to": data.get("evolvesTo"),
        "rules": data.get("rules"),
        "retreat_cost": data.get("retreatCost"),
        "converted_retreat_cost": data.get("convertedRetreatCost"),
        "number": data.get("number", ""),
        "artist": data.get("artist"),
        "rarity": data.get("rarity"),
        "national_pokedex_numbers": data.get("nationalPokedexNumbers"),
        "small_image": data.get("images", {}).get("small"),
        "large_image": data.get("images", {}).get("large"),
        "set": card_set,
    }
    obj, _ = Card.objects.update_or_create(
        card_id=data.get("id"), defaults=defaults
    )
    return obj


def _update_attacks(card: Card, attacks: List[dict[str, Any]]) -> None:
    """Replace attack records for a card."""

    Attack.objects.filter(card=card).delete()
    for atk in attacks:
        Attack.objects.create(
            card=card,
            name=atk.get("name", ""),
            cost=atk.get("cost"),
            converted_energy_cost=atk.get("convertedEnergyCost", 0),
            damage=atk.get("damage", ""),
            text=atk.get("text"),
        )


def _update_weaknesses(card: Card, weaknesses: List[dict[str, Any]]) -> None:
    """Replace weakness records for a card."""

    Weakness.objects.filter(card=card).delete()
    for wk in weaknesses:
        Weakness.objects.create(
            card=card, type=wk.get("type", ""), value=wk.get("value", "")
        )


def _update_tcgplayer(card: Card, tcgplayer: dict[str, Any]) -> None:
    """Create or update TCGPlayer pricing info."""

    if not tcgplayer:
        return

    defaults = {
        "url": tcgplayer.get("url", ""),
        "updated_at": _parse_date(tcgplayer.get("updatedAt")),
    }
    prices = tcgplayer.get("prices", {}).get("holofoil", {})
    defaults.update(
        {
            "low": prices.get("low"),
            "mid": prices.get("mid"),
            "high": prices.get("high"),
            "market": prices.get("market"),
            "direct_low": prices.get("directLow"),
        }
    )
    TCGPlayerPrice.objects.update_or_create(card=card, defaults=defaults)
