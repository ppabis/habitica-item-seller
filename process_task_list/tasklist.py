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
    with fields `id`, `date` (can be None), `difficulty`, `attribute`,
    `title` and `notes` (can be None).

    ```text
    ID    due date   difficulty+attribute - task description [notes]
    0001. 15/07/2024 TP - Wash the dishes
    0002.            HI - Create a new blog post [notes here]
    ```
    """
    r = re.match('^(\\d+).\\s+([0-9/]*)\\s*([TEMHtemh])([SIPCsipc])\\s+-\\s+([^\\[]*)(\\[.*\\])?$', line)
    if r:
        # Try to parse the date first, return None if invalid
        try:
            date = None if r.group(2) == '' else dt.strptime(r.group(2), '%d/%m/%Y')
        except ValueError:  # Only catch invalid date formats
            return None
        
        difficulty = DIFFICULTIES[r.group(3).upper()]
        attribute = ATTRIBUTES[r.group(4).upper()]
        title = r.group(5).strip()
        notes = r.group(6).strip()[1:-1] if r.group(6) else None
        return {
            'id': r.group(1),
            'date': date,
            'difficulty': difficulty,
            'attribute': attribute,
            'title': title,
            'notes': notes
        }
    return None


def parse_task_list(task_list: str) -> list[dict]:
    """
    Parse a file with tasks. Each line will be processed by
    `line_to_task` function. Invalid lines will be skipped.
    """
    tasks = []
    for line in task_list.split('\n'):
        try:
            task = line_to_task(line.strip())
            if task:
                tasks.append(task)
        except Exception as e:
            print(f"Error processing line '{line}': {e}")
    return tasks
