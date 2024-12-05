sample_rule_1 = {
    "rules": [
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
    "actions": [
        {"type": "move", "value": "Important"},
        {"type": "unread_flag", "value": "true"},
    ],
}
