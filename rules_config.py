sample_rule = {
    "rules": {
        "conditions": [
            {
                "field": "from_address",
                "predicate": "contains",
                "value": "linkedin",
            },
            {
                "field": "date_received",
                "predicate": "less than days",
                "value": 10,
            },
        ],
        "match": "all",
    },
    "actions": {
        "move": "TRASH",
        "mark": ["UNREAD"],
    },
}
