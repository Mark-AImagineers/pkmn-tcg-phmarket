import requests
from django.utils.timezone import now
from cards.models import CardRef

BASE_URL = "https://api.pokemontcg.io/v2/cards"
PAGE_SIZE = 250


def discover_all_cards_ids():
    """
    Discover all known cards IDS from pokeTCG and store them in CardRef
    
    This function paginates through the /cards endpoints and insters any new card IDs
    into the CardRef table if they are not already present.
    """
    page = 1
    while True:
        res = requests.get(
            BASE_URL,
            params={"page": page, "pageSize": PAGE_SIZE},
            timeout=30,
        )

        if res.status_code != 200:
            print(f"Failed to fetch page {page}: {res.status_code}")
            break

        data = res.json().get("data", [])
        if not data:
            break

        print(f"Fetched {len(data)} cards from page {page}")
        page += 1

        for card in data:
            card_id = card.get("id", "").strip()
            if not card_id:
                continue

            # Only create if it doesn't already exist
            if not CardRef.objects.filter(card_id=card_id).exists():
                CardRef.objects.create(card_id=card_id)