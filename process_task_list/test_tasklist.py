import pytest
from datetime import datetime as dt
from .tasklist import line_to_task, parse_task_list

def test_line_to_task_valid_cases():
    # Test case with date and no notes
    result = line_to_task("0001. 15/07/2024 TP - Wash the dishes")
    assert result == {
        'id': '0001',
        'date': dt.strptime('15/07/2024', '%d/%m/%Y'),
        'difficulty': '0.1',
        'attribute': 'per',
        'title': 'Wash the dishes',
        'notes': None
    }

    # Test case without date but with notes
    result = line_to_task("0002. HI - Create a blog post [Draft the outline first]")
    assert result == {
        'id': '0002',
        'date': None,
        'difficulty': '2',
        'attribute': 'int',
        'title': 'Create a blog post',
        'notes': 'Draft the outline first'
    }

    # Test case with lowercase difficulty and attribute
    result = line_to_task("0003. ms - Study for exam")
    assert result == {
        'id': '0003',
        'date': None,
        'difficulty': '1.5',
        'attribute': 'str',
        'title': 'Study for exam',
        'notes': None
    }

def test_line_to_task_invalid_cases():
    # Invalid format cases should return None
    assert line_to_task("") is None
    assert line_to_task("Not a task") is None
    assert line_to_task("0001. 15/07/2024 XX - Invalid difficulty") is None
    assert line_to_task("abc. 15/07/2024 TP - Invalid ID") is None
    assert line_to_task("0001. 15/13/2024 TP - Invalid date") is None

def test_parse_task_list():
    task_list = """0001. 15/07/2024 TP - Wash the dishes
0002. HI - Create a blog post [Draft outline]
Invalid line
0003. MS - Study for exam
"""
    results = parse_task_list(task_list)
    
    assert len(results) == 3
    
    # Check first task
    assert results[0]['id'] == '0001'
    assert results[0]['date'] == dt.strptime('15/07/2024', '%d/%m/%Y')
    assert results[0]['difficulty'] == '0.1'
    assert results[0]['attribute'] == 'per'
    
    # Check second task
    assert results[1]['id'] == '0002'
    assert results[1]['date'] is None
    assert results[1]['difficulty'] == '2'
    assert results[1]['attribute'] == 'int'
    assert results[1]['notes'] == 'Draft outline'
    
    # Check third task
    assert results[2]['id'] == '0003'
    assert results[2]['date'] is None
    assert results[2]['difficulty'] == '1.5'
    assert results[2]['attribute'] == 'str'

def test_parse_task_list_empty():
    assert parse_task_list("") == []
    assert parse_task_list("\n\n") == []
