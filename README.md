Habitica Automations on Lambda
=============================
This project creates a Lambda function that authenticates with Habitica in order
to sell excess items from the user's inventory.

Another function collects statistics of the player into a Timestream database.

The functions run on a schedule with EventBridge. Because of rate limiting on
Habitica's side, there need to be several schedules to ensure that we don't
overwhelm the Habitica API (30 requests per minute).