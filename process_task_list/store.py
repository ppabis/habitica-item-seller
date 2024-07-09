import boto3, os

TABLE_NAME = os.environ['TABLE_NAME']
ddb = boto3.resource('dynamodb').Table(TABLE_NAME)

def compare_and_update(task: dict, item: dict) -> dict | None:
    """
    Compares the task found in the list and the task found in DynamoDB.
    Returns a DynamoDB item that should be updated. If the items are
    not to be updated (are almost equal), returns None.

    Equality here is defined if the fields of the task are the same as
    item in DynamoDB. However, as the table will hold some more attributes,
    such as UUID from Habitica and the completion status, we should only
    compare those.
    """
    dirty = False
    task['date'] = task['date'].isoformat() if task['date'] else ""
    
    if task['title'] != item['title']:
        item['title'] = task['title']
        dirty = True
    
    if task['date'] != item['date']:
        item['date'] = task['date']
        dirty = True
    
    if task['difficulty'] != item['difficulty']:
        item['difficulty'] = task['difficulty']
        dirty = True
    
    if task['attribute'] != item['attribute']:
        item['attribute'] = task['attribute']
        dirty = True
    
    return item if dirty else None


def create_task(task: dict) -> dict:
    """
    Formats a task as a new DynamoDB row.
    """
    return {
        'id': task['id'],
        'title': task['title'],
        'date': task['date'].isoformat() if task['date'] else "",
        'difficulty': task['difficulty'],
        'attribute': task['attribute'],
    }


def store_update_tasks(tasks: list[dict]) -> list[str]:
    """
    First checks if task exists. If it exists, compare the contents.
    If it is different, update the task. Otherwise, skip it.
    If it does not exist, create a new task.

    Returns the list of primary keys of items that we created or
    updated.
    """
    ids = []
    for task in tasks:
        # Update a task if it is different
        response = ddb.get_item(Key={'id': task['id']})
        if 'Item' in response:
            updated = compare_and_update(task, response['Item'])
            if updated:
                ddb.put_item(Item=updated)
                ids.append(task['id'])
            else:
                print(f"Task {task['id']} is up to date.")
        # Task not found so create a new one
        else:
            ddb.put_item(Item=create_task(task))
            ids.append(task['id'])
    
    return ids
    