import os, json
from boto3 import client

def get_secret(habitica):
    """
    Retrieves the secret from AWS Secrets Manager.
    """
    secrets = client("secretsmanager")
    secret = secrets.get_secret_value(SecretId=habitica)
    secret = json.loads(secret['SecretString'])
    return list(secret.items())[0]


def get_headers() -> dict:
    """
    Produces a list of headers that are required for Habitica API requests.
    """
    # By default try to load environment variables.
    HABITICA_USER=os.getenv('HABITICA_USER')
    HABITICA_KEY=os.getenv('HABITICA_KEY')
    
    # But if there's HABITICA_SECRET set, use Secrets Manager.
    HABITICA_SECRET=os.getenv('HABITICA_SECRET')
    if HABITICA_SECRET:
        print('Using Secrets Manager.')
        HABITICA_USER, HABITICA_KEY = get_secret(HABITICA_SECRET)

    HABITICA_CLIENT=f"{HABITICA_USER}-itemseller10"
    print(f"Client {HABITICA_CLIENT}")
    
    return {
        "x-api-user": HABITICA_USER,
        "x-api-key": HABITICA_KEY,
        "x-client": HABITICA_CLIENT
    }