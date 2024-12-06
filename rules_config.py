sample_rule = {
    "rules": {
        "conditions": [
            {
                "field": "from_address",
                "predicate": "contains",
                "value": "naukri",
            },
        ],
        "match": "all",
    },
    "actions": {
        "move": "INBOX",
        "mark": ["READ"],
    },
}
