from auth import get_headers
from database import get_formatted_task
from actions import update_task

HEADERS = get_headers()

def lambda_handler(event, context):
    tasks = event.get('List', [])
    
    if not tasks:
        event['Finished'] = True
        return event

    task = event['List'][0]

    try:
        uuid, task = get_formatted_task(task)
        update_task(HEADERS, uuid, task)
    except Exception as e:
        # Event if we catch exception, we just continue with the next task
        # to process
        print(e)

    # Remove first element and return the list
    event['List'] = event['List'][1:]
    # If the list is empty, inform the Step Function that we are done
    event['Finished'] = len(event['List']) == 0
    
    return event