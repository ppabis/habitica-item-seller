import boto3

def store_in_timestream(database: str, table: str, timestamp: float, username: str, stats: dict):
    """
    Stores the stats in Amazon Timestream.
    """
    dimensions = [ {'Name': 'username', 'Value': username} ]
    client = boto3.client('timestream-write')

    records = [
        {
            'Dimensions': dimensions,
            'MeasureName': stat,
            'MeasureValue': str(value),
            'MeasureValueType': 'DOUBLE',
            'Time': str(int(timestamp * 1000)),
            'TimeUnit': 'MILLISECONDS',
        }
        for stat, value in stats.items()
    ]
    
    client.write_records(DatabaseName=database, TableName=table, Records=records)