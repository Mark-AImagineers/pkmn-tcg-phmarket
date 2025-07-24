import requests
import os
import time
import math
from django.utils.timezone import now
from cards.models import CardRef

BASE_URL = "https://api.pokemontcg.io/v2/cards"
PAGE_SIZE = 250
POKETCG_API_KEY = os.environ.get("POKETCG_API")

HEADERS = {
    "X-Api-Key": POKETCG_API_KEY,
    "User-Agent": "PKMNTCGPH-SyncDev/0.1 (contact: markb@aimagineers.io)",
}

def discover_all_cards_ids():
    """
    Discover all known cards IDS from pokeTCG and store them in CardRef
    
    This function paginates through the /cards endpoints and insters any new card IDs
    into the CardRef table if they are not already present.
    """
    try:
        res = requests.get(
            BASE_URL,
            params={"page":1, "pageSize":1},
            headers=HEADERS,
            timeout=60,
        )
        res.raise_for_status()
        total_count = res.json().get("totalCount", 0)
    except Exception as e:
        print(f"❌ Failed to get total card count: {e}")
        return
    
    if total_count == 0:
        print("❌ totalCount returned 0. Aborting.")
        return

    max_pages = math.ceil(total_count / PAGE_SIZE)
    print(f"🔍 Discovered total {total_count} cards across {max_pages} pages.")



    for page in range (1, max_pages + 1):

        retries = 0
        while retries < 5:
            try:
                res = requests.get(
                    BASE_URL,
                    params={"page": page, "pageSize": PAGE_SIZE},
                    headers=HEADERS,
                    timeout=60,
                )
                if res.status_code == 200:
                    break # success
                else:
                    print(f"Page {page} failed with status {res.status_code}, retrying...")
            except requests.RequestException as e:
                print(f"Request error on page {page}: {e}, retrying...")

            retries +=1
            time.sleep(0.5 * (2 ** retries)) #exponential backoff

        if retries == 5:
            print(f"❌ Skipping page {page} after 5 failed retries.")
            continue

        data = res.json().get("data", [])
        inserted = 0
        skipped = 0
        exists = 0
        if not data:
            break

        print(f"Fetched {len(data)} cards from page {page}")

        for card in data:
            card_id = card.get("id", "").strip()
            if not card_id:
                skipped += 1
                continue
            
            if not CardRef.objects.filter(card_id=card_id).exists():
                CardRef.objects.create(card_id=card_id)
                inserted += 1
            else:
                exists += 1

        print(f"📦 Page {page}: ✅ {inserted} new, ⚠️ {exists} already existed, ❌ {skipped} skipped")

def get_cardref_count() -> int:
    """
    Returns the total number of card IDs discovered and saved in CardRef
    """
    return CardRef.objects.count()

