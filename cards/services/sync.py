from cards.models import CardRef, Card, CardSet
from django.db import transaction
from cards.services.discovery import HEADERS
import requests
import time

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
        #Save card in db here
        print(f"⬇️ Fetched Card: {data.get('name')} ({card_id})")
        # TODO: Parse and save to models

        synced += 1
    
    return synced