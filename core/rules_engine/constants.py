""" This contains constants for the rules engine. """


from typing import Final


class RulesEngineConstants:
    STRING_FIELDS: Final[list[str]] = ["from_address", "to_address", "subject"]
    DATETIME_FIELDS: Final[list[str]] = ["date_received"]
