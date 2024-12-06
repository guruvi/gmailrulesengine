""" This module defines the logic for applying rules on the email data. """


from typing import Any
from gmail_rules_engine.tables import Email
from piccolo.columns.combination import And, Or, Where
from datetime import datetime, timedelta


def construct_query(rule_config: dict) -> And | Or:
    """
    Construct a query string based on the rule.

    :param rule: Rule
    :type rule: dict

    :return: Query string
    :rtype: str
    """
    rules: dict[str, Any] = rule_config["rules"]
    where_clauses: list[Any] = match_conditions(conditions=rules["conditions"])
    combined_clauses: And | Or = combine_where_clauses(
        where_clauses=where_clauses, matcher=rules["match"]
    )
    return combined_clauses


def match_conditions(*, conditions: list[dict[str, Any]]) -> list[Where]:
    """
    Matches the given conditions and returns a list of where clauses.

    Args:
        conditions (list[dict[str, Any]]): The list of conditions to match.

    Returns:
        list[Any]: The list of where clauses.

    Raises:
        NotImplementedError: If the rule type is not implemented.
    """
    where_clauses: list[Any] = []
    for rule in conditions:
        match rule["type"]:
            case "string":
                where_clauses.append(
                    column_match_for_str_types(
                        field_name=rule["field"],
                        value=rule["value"],
                        predicate=rule["predicate"],
                    )
                )
            case "datetime":
                where_clauses.append(
                    column_match_for_datetime_types(
                        field_name=rule["field"],
                        value=rule["value"],
                        predicate=rule["predicate"],
                    )
                )
            case _:
                raise NotImplementedError("Rule type not implemented.")
    return where_clauses


def combine_where_clauses(*, where_clauses: list[Any], matcher: str) -> And | Or:
    """
    Combines the where clauses based on the matcher.

    Args:
        where_clauses (list[Any]): The list of where clauses.
        matcher (str): The matcher to use.

    Returns:
        Any: The combined where clause.
    """
    filter_query: And | Or = where_clauses[0]

    for clause in where_clauses[1:]:
        match matcher:
            case "all":
                filter_query &= clause
            case "any":
                filter_query |= clause
            case _:
                raise NotImplementedError("Rule combination not implemented.")

    return filter_query


def fetch_column_name(*, field_name: str) -> str:
    """
    Fetch the column names from the Email table.

    :param field_name: Field name
    :type field_name: str

    :return: Column name
    :rtype: str
    """
    field_name_with_lowercase = field_name.lower() if field_name else ""
    match field_name_with_lowercase:
        case "from_address":
            return Email.from_address
        case "to_address":
            return Email.to_address
        case "subject":
            return Email.subject
        case "date":
            return Email.date_received
        case _:
            raise AttributeError("Invalid field name")


def column_match_for_str_types(*, field_name: str, value: str, predicate: str) -> str:
    """
    This method contains the logic for applying rules on string types.

    :param field_name: Field name
    :type field_name: str

    :param value: Value
    :type value: str

    :param predicate: Predicate
    :type predicate: str

    :return: Query string
    :rtype: str
    """
    match predicate.lower():
        case "equals":
            return fetch_column_name(field_name=field_name) == value
        case "not equals":
            return fetch_column_name(field_name=field_name) != value
        case "contains":
            return fetch_column_name(field_name=field_name).like(f"%{value}%")
        case "does not contains":
            return fetch_column_name(field_name=field_name).not_like(f"%{value}%")
        case _:
            raise NotImplementedError("Rule type not implemented.")


def column_match_for_datetime_types(
    *, field_name: str, value: int, predicate: str
) -> str:
    """
    This method contains the logic for applying rules on datetime types.

    :param field_name: Field name
    :type field_name: str

    :param value: value
    :type value: int

    :param predicate: Predicate
    :type predicate: str

    :return: Query string
    :rtype: str
    """
    current_datetime: datetime.datetime = datetime.now(tz=datetime.timezone.utc)
    match predicate.lower():
        case "less than days":
            return fetch_column_name(
                field_name=field_name
            ) > current_datetime - timedelta(days=value)
        case "greater than days":
            return fetch_column_name(
                field_name=field_name
            ) < current_datetime - timedelta(days=value)
        case _:
            raise NotImplementedError("Rule type not implemented.")
