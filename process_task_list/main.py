from tasklist import parse_task_list
from store import store_update_tasks
from boto3 import client

s3 = client('s3')

def process_file(record) -> list[str]:
    """
    Read the file from S3 and stores the tasks in DynamoDB formatted
    and processed appropriately.
    """
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']
    obj = s3.get_object(Bucket=bucket, Key=key)
    tasks = parse_task_list(obj['Body'].read().decode('utf-8'))
    ids = store_update_tasks(tasks)
    print(f"Updated or created tasks: {', '.join(ids)}")
    return ids

def lambda_handler(event, context):
    ids = []
    for record in event['Records']:
        if record['eventName'].startswith('ObjectCreated'):
            try:
                ids.extend( process_file(record) )
            except Exception as e:
                print(f"Error processing record: {e}")
    ids.append("_END_")
    return {
            'statusCode': 200,
            'body': ids
        }