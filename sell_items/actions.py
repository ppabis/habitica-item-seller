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


def is_event_valid(event) -> bool:
    """
    Validates the event so that sell_category is present and correct.
    """
    return ('sell_category' in event)\
          and (event['sell_category'] in ['food', 'eggs', 'hatchingPotions'])


def sell_items(headers: dict, items_to_leave: int, event) -> float:
    """
    Sells items of a specific category in `event['sell_category']`.
    We need to sell items only in the category specified to not sell too much at once.
    """
    if not is_event_valid(event):
        print("No sell_category specified!")
        raise ValueError("Missing 'sell_category' key in event. And such, ignoring this event.")
    
    category = event['sell_category']
    
    items, gold = get_inventory(headers)
    print(f"Starting with gold [{category}] {gold:.2f}.")
    items_to_sell = items[category]

    # Filter items that we have more than threshold.
    items_to_sell = {k: v for k, v in items_to_sell.items() if v > items_to_leave}
    
    # Print history of what is being done.
    string_items = ", ".join([f"{k} ({v})" for k, v in items_to_sell.items()])
    print(f"Items to sell [{category}]: {string_items}")
    
    last_sale = None
    # Sell items.
    for item, amount in items_to_sell.items():
        count = amount - items_to_leave
        print(f"Selling {count} of {item}.")
        try:
            _sold = sell_item(headers, event['sell_category'], item, count)
        except Exception as e:
            print(f"Failed to sell {item}: {e}.")
            continue
        last_sale = _sold
        print(f"Sold {count} of {item}.")
    
    if last_sale is not None:
        gp = last_sale['data']['stats']['gp']
        print(f"Gold after sale [{category}]: {gp:.2f}. Made {gp - gold:.2f} gold.")
    else:
        print(f"Didn't sell anything for {category}.")

    return gp - gold