from tasklist import parse_task_list
from store import store_update_tasks
from boto3 import client
import os, json

s3 = client('s3')
step = client('stepfunctions')
STEP_FUNCTION_NAME = os.getenv('STEP_FUNCTION_NAME')

def process_file(record) -> list[str]:
    """
    Read the file from S3 and stores the tasks in DynamoDB formatted
    and processed appropriately.
    """
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']
    obj = s3.get_object(Bucket=bucket, Key=key)
    tasks = parse_task_list(obj['Body'].read().decode('utf-8'))
    print(f"len(tasks) = {len(tasks)}")
    ids = store_update_tasks(tasks)
    print(f"Tasks to update: {', '.join(ids)}")
    return ids

def lambda_handler(event, context):
    ids = []
    for record in event['Records']:
        if record['eventName'].startswith('ObjectCreated'):
            try:
                _ids = process_file(record)
                ids.extend(_ids)
            except Exception as e:
                print(f"Error processing record: {e}")

    # If the lists are empty, we don't have to even execute the Step Function
    if len(ids) > 0 and STEP_FUNCTION_NAME:
        print(f"Starting Step Function {STEP_FUNCTION_NAME} with {len(ids)} tasks.")
        step.start_execution(stateMachineArn=STEP_FUNCTION_NAME, input=json.dumps({"List": ids, "Finished": False}))
    
    return {
            'statusCode': 200,
            'body': {
                'List': ids,
                'Finished': len(ids) == 0
            }
        }