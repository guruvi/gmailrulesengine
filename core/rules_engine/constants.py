""" This contains constants for the rules engine. """


from typing import Final


class RulesEngineConstants:
    STRING_FIELDS: Final[list[str]] = ["from_address", "to_address", "subject"]
    DATETIME_FIELDS: Final[list[str]] = ["date_received"]

class StringFieldPredicates:
    EQUALS: Final[str] = "equals"
    NOT_EQUALS: Final[str] = "not equals"
    CONTAINS: Final[str] = "contains"
    DOES_NOT_CONTAINS: Final[str] = "does not contains"

class DateTimeFieldPredicates:
    LESS_THAN_DAYS: Final[str] = "less than days"
    GREATER_THAN_DAYS: Final[str] = "greater than days"

class RulesPredicate:
    ALL: Final[str] = "all"
    ANY: Final[str] = "any"
