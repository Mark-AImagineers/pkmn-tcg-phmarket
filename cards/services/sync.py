from cards.models import CardRef, Card, CardSet
from django.db import transaction
from cards.services.discovery import HEADERS
from datetime import datetime
import requests
import time

def _parse_date(value: str):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        try:
            return datetime.strptime(value, "%Y/%m/%d").date()
        except ValueError:
            return None

def get_missing_cards_ids() -> list[str]:
    """
    Returns a list of card_ids that are present in CardRef
    but not yet fetched into the Card Table.
    """
    ref_ids = CardRef.objects.values_list("card_id", flat=True)
    fetched_ids = Card.objects.values_list("card_id", flat=True)

    missing_ids = set(ref_ids) - set(fetched_ids)
    return list(missing_ids)

def fetch_and_sync_cards(cards_ids: list[str]) -> int:
    """
    Fetches full card data from PokeTCG and saves it into the database.
    Returns number of cards successfully created
    """

    synced = 0

    for card_id in cards_ids:
        retries = 0
        while retries < 5:
            try:
                res = requests.get(
                    f"https://api.pokemontcg.io/v2/cards/{card_id.strip()}",
                    headers=HEADERS,
                    timeout=60,
                )
                if res.status_code == 200:
                    break
                elif res.status_code == 404:
                    print(f"❌ Card {card_id} not found (404). Skipping")
                    CardRef.objects.filter(card_id=card_id).update(error=True)
                    break
                else:
                    print(f"Card {card_id} failed with status {res.status_code}, retrying...")
            except requests.RequestException as e:
                print(f"Request error on card {card_id}: {e}, retrying...")

            retries += 1
            time.sleep(0.5 * (2 ** retries))

        if retries == 5 or res.status_code != 200:
            print(f"❌ Skipping card {card_id} after 5 retries")
            continue

        data = res.json().get("data", {})

        #parse and save CardSet
        set_data = data.get("set", {})
        set_obj, _ = CardSet.objects.get_or_create(
            set_id=set_data["id"],
            defaults={
                "name": set_data["name"],
                "series": set_data["series"],
                "printed_total": set_data.get("printedTotal", 0),
                "total": set_data.get("total", 0),
                "ptcgo_code": set_data.get("ptcgoCode"),
                "release_date": _parse_date(set_data.get("releaseDate", "")),
                "updated_at": _parse_date(set_data.get("updatedAt", "")),
                "symbol_image": set_data.get("images", {}).get("symbol"),
                "logo_image": set_data.get("images", {}).get("logo"),
            },
        )

        card_obj = Card.objects.create(
            card_id=data["id"],
            name=data["name"],
            supertype=data.get("supertype", ""),
            subtypes=data.get("subtypes"),
            hp=data.get("hp"),
            types=data.get("types"),
            evolves_to=data.get("evolvesTo"),
            rules=data.get("rules"),
            retreat_cost=data.get("retreatCost"),
            converted_retreat_cost=data.get("convertedRetreatCost"),
            number=data["number"],
            artist=data.get("artist"),
            rarity=data.get("rarity"),
            national_pokedex_numbers=data.get("nationalPokedexNumbers"),
            small_image=data.get("images", {}).get("small"),
            large_image=data.get("images", {}).get("large"),
            set=set_obj,
        )

        for atk in data.get("attacks", []):
            card_obj.attacks.create(
                name=atk.get("name"),
                cost=atk.get("cost"),
                converted_energy_cost=atk.get("convertedEnergyCost", 0),
                damage=atk.get("damage", ""),
                text=atk.get("text"),
            )

        for weak in data.get ("weaknesses", []):
            card_obj.weaknesses.create(
                type=weak.get("type", ""),
                value=weak.get("value", ""),
            )

        print(f"⬇️ Fetched Card: {data.get('name')} ({card_id})")

        synced += 1
    
    return synced