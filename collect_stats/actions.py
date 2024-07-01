import requests, boto3

HABITICA_URL="https://habitica.com/api/v3"

STATS_TO_GET = ['gp', 'exp', 'mp', 'lvl', 'hp']

def filter_stats(stats: dict) -> dict:
    """
    Filters the stats to only include the ones we care about.
    """
    return {k: v for k, v in stats.items() if k in STATS_TO_GET}


def get_stats(headers: dict) -> tuple[str, dict]:
    """
    Gets user stats: gold, exp, level, hp, etc.
    Returns a dict of username and all the collected stats.
    """
    url = f"{HABITICA_URL}/user?userFields=stats"
    response = requests.get(url, headers=headers)
    code = response.status_code
    if code == 200:
        user = response.json()['data']['auth']['local']['username']
        stats = filter_stats(response.json()['data']['stats'])
        return user, stats
    raise Exception(response.json()['message'])

