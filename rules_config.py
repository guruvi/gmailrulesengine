sample_rule = {
    "rules": {
        "conditions": [
            {
                "field": "from_address",
                "type": "string",
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
