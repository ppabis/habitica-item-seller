from actions import get_inventory, sell_item
from auth import get_headers
import os

HEADERS = get_headers()
# This is the amount of each item that will be left and not sold.
ITEMS_TO_LEAVE = int(os.getenv('ITEMS_TO_LEAVE', "25"))

def lambda_handler(event, context):
    items, gold = get_inventory()
    return {
        "statusCode": 200,
        "body": items
    }

if __name__ == "__main__":
    from pprint import pprint
    
    items, gp = get_inventory(HEADERS)
    food = items['food']
    
    print(f">> Current gold {gp:.2f}. Food:")
    pprint(food)

    if food['CottonCandyBlue'] > 30:
        sold = sell_item(HEADERS, 'food', 'CottonCandyBlue', 2)
    
    items, gp = get_inventory(HEADERS)
    food = items['food']
    print(f">> After sale, gold: {gp:.2f}. Food:")
    pprint(food)