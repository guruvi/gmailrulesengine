sample_rule = {
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
}
