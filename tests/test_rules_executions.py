from unittest import mock

from core.rules_executions import execute


@mock.patch("core.rules_executions.construct_query")
@mock.patch("core.rules_executions.filter_emails")
@mock.patch("core.rules_executions.execute_gmail_actions")
def test_rules_executions(mock_gmail_actions, mock_filter_emails, mock_construct_query):
    execute(
        user_id="abcde@gmail.com",
        config_dict={
            "rules": {
                "conditions": [
                    {
                        "field": "from_address",
                        "type": "string",
                        "predicate": "contains",
                        "value": "ktkbank.in",
                    },
                    {
                        "field": "subject",
                        "type": "string",
                        "predicate": "contains",
                        "value": "Secret to building wealth! Click now",
                    },
                ],
                "match": "all",
            },
            "actions": {
                "move": "INBOX",
                "mark": ["UNREAD", "IMPORTANT"],
            },
        },
    )
    # Assertions to be completed
