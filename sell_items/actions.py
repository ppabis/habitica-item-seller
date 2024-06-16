import requests
from filters import filter_items

HABITICA_URL="https://habitica.com/api/v3"

def get_inventory(headers: dict) -> tuple[dict, float]:
    """
    Gets user inventory in the form of eggs, potions, food and stats (gold).
    Items are filtered for the most common ones.
    Returns a tuple of (items: dict, gold: float).
    """
    url = f"{HABITICA_URL}/user?userFields=stats,items.eggs,items.hatchingPotions,items.food"
    response = requests.get(url, headers=headers)
    code = response.status_code
    if code == 200:
        items = response.json()['data']['items']
        gold = response.json()['data']['stats']['gp']
        return filter_items(items), gold
    raise Exception(response.json()['message'])


def sell_item(headers: dict, item_type: str, item_key: str, count: int):
    """
    Sells a specific item with the given count.
    1:1 mapping of Habitica API documentation.
    """
    url = f"{HABITICA_URL}/user/sell/{item_type}/{item_key}?amount={count}"
    response = requests.post(url, headers=headers)
    code = response.status_code
    if code == 200:
        return response.json()
    raise Exception(response.json()['message'])