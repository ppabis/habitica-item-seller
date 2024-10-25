import boto3, os
from actions import batch_create_tasks

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
    task['notes'] = task['notes'] if task['notes'] else ""
    
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

    # It can happen that the notes are not present in the item so that's why
    # we first check if they are present and only then compare. Otherwise, we just
    # add the notes to the item.
    if 'notes' in item:
        if task['notes'] != item['notes']:
            item['notes'] = task['notes']
            dirty = True
    else:
        if task['notes']:
            item['notes'] = task['notes']
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
        'notes': task['notes'] if task['notes'] else ""
    }


def store_update_tasks(tasks: list[dict]) -> list[str]:
    """
    First checks if task exists. If it exists, compare the contents.
    If it is different, update the task. Otherwise, skip it.
    If it does not exist, create a new task.

    Returns the list of primary keys of items that have to be yet updated
    in Habitica API.
    """
    updated_ids, new_tasks = [], []
    for task in tasks:
        # Update a task if it is different
        response = ddb.get_item(Key={'id': task['id']})
        if 'Item' in response:
            updated = compare_and_update(task, response['Item'])
            if updated:
                ddb.put_item(Item=updated)
                print(f"Updated task {task['id']}.")
                # If the uuid is set, that means that task exists in Habitica
                if 'habitica_uuid' in updated and updated['habitica_uuid']:
                    updated_ids.append(updated['id'])
                else:
                    new_tasks.append(task)
            else:
                print(f"Task {task['id']} is up to date.")
        # Task not found so create a new one
        else:
            ddb.put_item(Item=create_task(task))
            new_tasks.append(task)
            print(f"Created new task {task['id']}.")

    # Create tasks in Habitica in batch
    ids_uuids = batch_create_tasks(new_tasks)

    # Update rows in DynamoDB to hold UUIDs from Habitica of recently created tasks
    for task_id, uuid in ids_uuids:
        try:
            ddb.update_item(
                Key={'id': task_id},
                UpdateExpression='SET habitica_uuid = :uuid',
                ExpressionAttributeValues={':uuid': uuid}
            )
            print(f"Added UUID {uuid} to task {task_id}.")
        except Exception as e:
            print(f"Error adding UUID to task {task_id}: {e}")
    
    return updated_ids
    