import requests

HABITICA_URL="https://habitica.com/api/v3"

def update_task(headers: dict, uuid: str, data: dict):
    """
    Updates a task in Habitica.
    """
    url = f"{HABITICA_URL}/tasks/{uuid}"
    
    response = requests.put(url, json=data, headers=headers)
    code = response.status_code
    if code == 200:
        return response.json()
    raise Exception(response.json()['message'])