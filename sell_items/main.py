from actions import sell_items
from auth import get_headers
import os, json

HEADERS = get_headers()
# This is the amount of each item that will be left and not sold.
ITEMS_TO_LEAVE = int(os.getenv('ITEMS_TO_LEAVE', "150"))

def lambda_handler(event, context):
    if event is str:
        event: dict = json.loads(event)
    
    try:
        gp = sell_items(HEADERS, ITEMS_TO_LEAVE, event)
    except Exception as e:
        return {
            "statusCode": 400,
            "body": str(e)
        }
    
    return {
        "statusCode": 200,
        "body": "Earned {gp:.2f} gold."
    }