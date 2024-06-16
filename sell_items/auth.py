import os

def get_headers() -> dict:
    """
    Produces a list of headers that are required for Habitica API requests.
    """
    HABITICA_USER=os.getenv('HABITICA_USER')
    HABITICA_KEY=os.getenv('HABITICA_KEY')
    HABITICA_CLIENT=f"{HABITICA_USER}-itemseller10"
    return {
        "x-api-user": HABITICA_USER,
        "x-api-key": HABITICA_KEY,
        "x-client": HABITICA_CLIENT
    }