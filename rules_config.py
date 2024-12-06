sample_rule = {
    "rules": {
        "conditions": [
            {
                "field": "to_address",
                "predicate": "contains",
                "value": "guru",
            },
            {
                "field": "date_received",
                "predicate": "less than days",
                "value": 1,
            },
        ],
        "match": "all",
    },
    "actions": {
        "move": "TRASH",
        "mark": ["READ"],
    },
}
