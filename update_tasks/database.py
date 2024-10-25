import boto3, os

TABLE_NAME = os.getenv('TABLE_NAME')

ddb = boto3.resource('dynamodb').Table(TABLE_NAME)


def get_formatted_task(task_id: str) -> tuple[str, dict]:
    """
    Retrieves the task formatted appropriately for Habitica. The first part of
    the tuple is Habitica UUID of the task. The second part is formatted task
    that can be directly submitted in `PUT` request. It can raise exception if
    task has no UUID or is not found in the table.
    """
    row = ddb.get_item(Key={'id': task_id})

    if 'Item' in row:

        if 'habitica_uuid' not in row['Item'] or not row['Item']['habitica_uuid']:
            raise Exception(f"Task {task_id} does not have a UUID!")

        task = row['Item']
        return task['habitica_uuid'], format_task(task)

    raise Exception(f"Task {task_id} not found!")


def format_task(task: dict) -> dict:
    """
    Similar to `create_task` from `process_task_list`. It allows only the
    appropriate fields to be passed to the API.
    """
    data = {
        "text": task['title'],
        "priority": task['difficulty'],
        "attribute": task['attribute'],
        "date": None, # Can be used for clearing the due date
        "notes": None
    }

    if 'date' in task and task['date']:
        data['date'] = task['date']

    if 'notes' in task and task['notes']:
        data['notes'] = task['notes']
    
    return data
