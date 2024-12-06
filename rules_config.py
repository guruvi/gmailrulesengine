sample_rule = {
    "rules": {
        "conditions": [
            {
                "field": "date",
                "type": "datetime",
                "predicate": "greater than days",
                "value": 100,
            },
        ],
        "match": "all",
    },
    "actions": {
        "move": "TRASH",
        "mark": ["READ", "UNIMPORTANT"],
    },
}
