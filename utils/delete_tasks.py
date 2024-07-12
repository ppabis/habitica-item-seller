import requests, os, boto3
from time import sleep

"""
What is this script?
It deletes all tasks in Habitica with specific TAG and all items in DynamoDB table. To be used
for development purposes.
How to use this?
1. Edit your TAG. All the tasks **MUST** be tagged!
2. Set your HABITICA_USER (user ID) and HABITICA_KEY (API key) as environment variables.
3. Make sure you have local AWS credentials set up. Use either env variables such as
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN or select a profile with AWS_PROFILE.
3. Run the script. 
You can lower SLEEP if you have less than 30 tasks, let's say down to 0.5
"""

# Change this to yours
TAG = "4aedf1fc-8dd7-4ff9-95f1-1f3112a0b815"
REGION = "eu-west-1"
TABLE_NAME = "HabiticaTaskList"
SLEEP = 2

def get_headers() -> dict:
    """
    Produces a list of headers that are required for Habitica API requests.
    """
    HABITICA_USER=os.getenv('HABITICA_USER')
    HABITICA_KEY=os.getenv('HABITICA_KEY')

    HABITICA_CLIENT=f"{HABITICA_USER}-itemseller10"
    print(f"Client {HABITICA_CLIENT}")
    
    return {
        "x-api-user": HABITICA_USER,
        "x-api-key": HABITICA_KEY,
        "x-client": HABITICA_CLIENT
    }

def get_tasks() -> list[dict]:
    """
    Retrieves all tasks from Habitica.
    """
    headers = get_headers()
    url = f"https://habitica.com/api/v3/tasks/user?type=todos"
    response = requests.get(url, headers=headers)
    code = response.status_code
    if code == 200:
        data = response.json()['data']
        data = [task for task in data if TAG in task['tags']]
        return data
    raise Exception(response.json()['message'])

def delete_all_dynamo_items():
    """
    Deletes all items from DynamoDB.
    """
    ddb = boto3.resource('dynamodb', region_name = REGION).Table(TABLE_NAME)
    items = ddb.scan()['Items']
    for item in items:
        print(f"Deleting {item['id']}")
        ddb.delete_item(Key={'id': item['id']})

def delete_task(task_id: str):
    """
    Deletes a task from Habitica.
    """
    headers = get_headers()
    url = f"https://habitica.com/api/v3/tasks/{task_id}"
    response = requests.delete(url, headers=headers)
    code = response.status_code
    if code == 200:
        return response.json()
    raise Exception(response.json()['message'])

if __name__ == "__main__":
    tasks = get_tasks()
    for task in tasks:
        print(f"Deleting {task['text']}")
        delete_task(task['id'])
        sleep(SLEEP)
    delete_all_dynamo_items()
    print("Done.")