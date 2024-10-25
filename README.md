Habitica Automations on Lambda
=============================

This project creates a Lambda function that authenticates with Habitica in order
to sell excess items from the user's inventory.

Another function collects statistics of the player into a Timestream database.

The functions run on a schedule with EventBridge. Because of rate limiting on
Habitica's side, there need to be several schedules to ensure that we don't
overwhelm the Habitica API (30 requests per minute).

Habitica Task Management
------------------------

This project provides tools for managing Habitica tasks, including:

- Processing task lists into Habitica-compatible format
- Automating task creation on Habitica

This Lambda runs via S3 event notification.

Task List Format
---------------

Tasks can be defined in a simple text format:

```text
ID    due date   difficulty+attribute - task description [optional notes]
0001. 15/07/2024 TP - Wash the dishes
0002.            HI - Create a blog post [Draft the outline first]
0003.            MS - Study for exam
```

### Each task line contains

- **ID**: A numeric identifier (e.g., 0001)
- **Due Date**: Optional date in DD/MM/YYYY format
- **Difficulty**: One of:
  - T (Trivial) = 0.1
  - E (Easy) = 1.0
  - M (Medium) = 1.5
  - H (Hard) = 2.0
- **Attribute**: One of:
  - S (Strength)
  - I (Intelligence)
  - P (Perception)
  - C (Constitution)
- **Title**: Task description
- **Notes**: Optional notes in square brackets. Use `<br>` to separate lines.
