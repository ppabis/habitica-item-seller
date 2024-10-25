import requests, os
from auth import get_headers

HABITICA_URL="https://habitica.com/api/v3"
TASK_TAG = os.getenv("TASK_TAG", "")

HEADERS = get_headers()

def batch_create_tasks(tasks) -> list[(str, str)]:
    """
    Creates a list of tasks in Habitica. Will return the tuples of our ID and UUID in Habitica or throw exception.
    """
    habitica_tasks = [create_task(task, TASK_TAG) for task in tasks]
    original_ids = [task['id'] for task in tasks]

    url = f"{HABITICA_URL}/tasks/user"
    response = requests.post(url, json=habitica_tasks, headers=HEADERS)
    code = response.status_code

    if code == 200 or code == 201:
        data = response.json()['data']
        uuids = [ t['id'] for t in data ] if isinstance(data, list) else [data['id']]
        return list(zip(original_ids, uuids))
    
    raise Exception(f"Exception from Habitica API when creating tasks: {response.json()['message']}")


def create_task(task: dict, tag: str = "") -> dict:
    """
    Prepares a new task for Habitica in the correct format expected by the API.
    """
    data = {
        "text": task['title'],
        "type": "todo",
        "priority": task['difficulty'],
        "attribute": task['attribute']
    }

    if 'date' in task and task['date']:
        data['date'] = task['date'].isoformat()
    
    if tag:
        data['tags'] = [tag]

    if 'notes' in task and task['notes']:
        data['notes'] = task['notes']
    
    return data
