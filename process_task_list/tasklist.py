import re
from datetime import datetime as dt

"""
For difficulties and attributes check the following API doc:
https://habitica.com/apidoc/#api-Task-CreateUserTasks
"""
DIFFICULTIES = { 'T': '0.1', 'E': '1', 'M': '1.5', 'H': '2' }
ATTRIBUTES = { 'S': 'str', 'I': 'int', 'P': 'per', 'C': 'con' }

def line_to_task(line: str) -> dict | None:
    """
    Processes the line to extract the task date. In case the line is not
    a valid task, returns None. If it is valid, it will return a dictionary
    with fields `id`, `date` (can be None), `difficulty`, `attribute` and
    `title`.

    ```text
    ID    due date   difficulty+attribute - task description
    0001. 15/07/2024 TP - Wash the dishes
    0002. none       HI - Create a new blog post
    ```
    """
    r = re.match('^(\\d+).\\s+([0-9/]+|none)\\s+([TEMHtemh])([SIPCsipc])\\s+-\\s+(.*)$', line)
    if r:
        date = None if r.group(2) == 'none' else dt.strptime(r.group(2), '%d/%m/%Y')
        difficulty = DIFFICULTIES[r.group(3).upper()]
        attribute = ATTRIBUTES[r.group(4).upper()]
        return {
            'id': r.group(1),
            'date': date,
            'difficulty': difficulty,
            'attribute': attribute,
            'title': r.group(5),
        }
    return None


def parse_task_list(task_list: str) -> list[dict]:
    """
    Parse a file with tasks. Each line will be processed by
    `line_to_task` function. Invalid lines will be skipped.
    """
    tasks = []
    for line in task_list.split('\n'):
        task = line_to_task(line.strip())
        if task:
            tasks.append(task)
    return tasks