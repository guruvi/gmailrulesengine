import datetime
from unittest import mock
import pytest

from piccolo.columns.combination import And, Or
from core.rules_engine.apply_rules import (
    column_match_for_datetime_types,
    column_match_for_str_types,
    construct_query,
    fetch_column_name,
)
from gmail_rules_engine.tables import Email


pytestmark = pytest.mark.applyrules


def test_fetch_column_name_valid():
    """
    Test fetch_column_name with valid field names.
    """
    # Ensure valid field names return the correct Email column
    assert fetch_column_name(field_name="from_address") == Email.from_address
    assert fetch_column_name(field_name="to_address") == Email.to_address
    assert fetch_column_name(field_name="subject") == Email.subject
    assert fetch_column_name(field_name="Date") == Email.date_received

    # Test case insensitivity
    assert fetch_column_name(field_name="FROM_ADDRESS") == Email.from_address
    assert fetch_column_name(field_name="To_Address") == Email.to_address
    assert fetch_column_name(field_name="sUbJeCt") == Email.subject
    assert fetch_column_name(field_name="date") == Email.date_received


@pytest.mark.parametrize("field_name", ["invalid_field", "", None])
def test_fetch_column_name_invalid(field_name):
    """
    Test fetch_column_name with invalid field names.
    """
    # Ensure invalid field names raise AttributeError
    with pytest.raises(AttributeError, match="Invalid field name"):
        fetch_column_name(field_name=field_name)


def test_column_matches_for_string_type_fields():
    """
    Test column_match_for_str_types for string type fields.
    """
    # Test the different predicates for string type fields
    _assert_column_value(
        column_match_for_str_types(
            field_name="from_address", value="ktkbank.in", predicate="equals"
        ),
        (Email.from_address == "ktkbank.in"),
    )
    _assert_column_value(
        column_match_for_str_types(
            field_name="from_address", value="ktkbank.in", predicate="not equals"
        ),
        (Email.from_address != "ktkbank.in"),
    )
    _assert_column_value(
        column_match_for_str_types(
            field_name="from_address", value="ktkbank.in", predicate="contains"
        ),
        (Email.from_address.like("%ktkbank.in%")),
    )
    _assert_column_value(
        column_match_for_str_types(
            field_name="from_address", value="ktkbank.in", predicate="does not contains"
        ),
        (Email.from_address.not_like("%ktkbank.in%")),
    )
    with pytest.raises(NotImplementedError) as ex:
        column_match_for_str_types(
            field_name="from_address", value="ktkbank.in", predicate="invalid_predicate"
        )


def test_column_matches_for_date_type_fields():
    """
    Test column matches for date type fields.
    """
    # Test the different predicates for string type fields
    current_utc_time: datetime.datetime = datetime.datetime.now(tz=datetime.timezone.utc)
    with mock.patch("core.rules_engine.apply_rules.datetime") as mock_datetime:
        mock_datetime.now.return_value = current_utc_time
        _assert_column_value(
            column_match_for_datetime_types(
                field_name="date", value=1, predicate="less than days"
            ),
            (Email.date_received > current_utc_time - datetime.timedelta(days=1)),
        )

        _assert_column_value(
            column_match_for_datetime_types(
                field_name="date", value=2, predicate="greater than days"
            ),
            (Email.date_received < current_utc_time - datetime.timedelta(days=2)),
        )


@mock.patch("core.rules_engine.apply_rules.datetime")
def test_construct_query_based_on_all_query_rules_match(mock_datetime):
    current_utc_time: datetime.datetime = datetime.datetime.now(tz=datetime.timezone.utc)
    mock_datetime.now.return_value = current_utc_time
    # Sample rule configurations
    all_rules_config = {
        "rules": {
            "match": "all",
            "conditions": [
                {
                    "field": "from_address",
                    "type": "string",
                    "predicate": "equals",
                    "value": "example.com",
                },
                {
                    "field": "subject",
                    "type": "string",
                    "predicate": "equals",
                    "value": "Hello World",
                },
                {
                    "field": "to_address",
                    "type": "string",
                    "predicate": "equals",
                    "value": "abc@gmail.com",
                },
            ],
        },
    }

    # Prepare the test data for Email table for testing the above rules
    and_query: And = construct_query(all_rules_config)
    assert type(and_query) == And
    assert and_query.get_column_values() == {
        Email.from_address: "example.com",
        Email.subject: "Hello World",
        Email.to_address: "abc@gmail.com",
    }


def test_construct_query_based_on_any_query_rules_match():
    # Sample rule configurations
    any_rules_config = {
        "rules": {
            "match": "any",
            "conditions": [
                {
                    "field": "from_address",
                    "type": "string",
                    "predicate": "equals",
                    "value": "example.com",
                },
                {
                    "field": "subject",
                    "type": "string",
                    "predicate": "equals",
                    "value": "Hello World",
                },
                {
                    "field": "to_address",
                    "type": "string",
                    "predicate": "equals",
                    "value": "abc@gmail.com",
                },
            ],
        },
    }

    # Prepare the test data for Email table for testing the above rules
    any_query = construct_query(any_rules_config)
    assert type(any_query) == Or


def _assert_column_value(column, expected_column):
    """
    Helper function to assert the column value.
    """
    assert column.column == expected_column.column
    assert column.operator == expected_column.operator
    assert column.value == expected_column.value
