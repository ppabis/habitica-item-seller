from actions import get_stats
from store import store_in_timestream
from auth import get_headers
import os, datetime

HEADERS = get_headers()
DATABASE_NAME = os.getenv('DATABASE_NAME')
TABLE_NAME = os.getenv('TABLE_NAME')

def lambda_handler(event, context):
    
    current_utc = datetime.datetime.now(datetime.UTC)
    current_utc_string = current_utc.strftime("%Y-%m-%d %H:%M:%S %Z")

    try:
        username, stats = get_stats(HEADERS)
        store_in_timestream(DATABASE_NAME, TABLE_NAME, current_utc.timestamp(), username, stats)
    except Exception as e:
        print(f"Error collecting stats at {current_utc_string}: {str(e)}")
        return {
            "statusCode": 500,
            "body": f"{current_utc_string}: {str(e)}"
        }
    
    print(f"Collected statistics for time {current_utc_string}.")
    return {
        "statusCode": 200,
        "body": f"Collected statistics for time {current_utc_string}."
    }

if __name__ == "__main__":
    u, st = get_stats(HEADERS)
    from pprint import pprint
    pprint(st)