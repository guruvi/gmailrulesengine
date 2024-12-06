""" This module contains different actions to be done on the messages. """


from unittest import mock
import pytest

from core.rules_engine.execute_actions import (
    convert_actions_to_labels,
    execute_gmail_actions,
)


pytestmark = pytest.mark.execute_actions


def move_label_only():
    return {
        "actions": {
            "move": "INBOX",
        }
    }


def mark_label_only():
    return {
        "actions": {
            "mark": ["UNREAD", "IMPORTANT"],
        }
    }


def mark_read_only():
    return {
        "actions": {
            "mark": ["READ"],
        }
    }


def move_and_mark_label():
    return {
        "actions": {
            "move": "INBOX",
            "mark": ["UNREAD", "UNIMPORTANT"],
        }
    }


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (move_label_only(), (["INBOX"], [])),
        (mark_label_only(), (["UNREAD", "IMPORTANT"], [])),
        (move_and_mark_label(), (["INBOX", "UNREAD"], ["IMPORTANT"])),
        (mark_read_only(), ([], ["UNREAD"])),
    ],
)
def test_convert_actions_to_labels(test_input, expected):
    """
    Test convert_actions_to_labels.
    """
    # Test the different actions
    assert convert_actions_to_labels(test_input) == expected


@mock.patch("core.rules_engine.execute_actions.batch_update_labels")
def test_should_invoke_gmail_actions_to_update_labels(mock_batch_update_labels):
    actions_config = {
        "actions": {
            "move": "INBOX",
            "mark": ["UNREAD", "UNIMPORTANT"],
        }
    }
    execute_gmail_actions(
        user_id="abcde@gmail.com",
        message_ids=["19380f65a0cd3791"],
        actions_config=actions_config,
    )
    # assert mock_batch_update_labels.assert_called_once(
    #     user_id="abcde@gmail.com",
    #     message_ids=["19380f65a0cd3791"],
    #     add_labels=["INBOX", "UNREAD"],
    #     remove_labels=["IMPORTANT"],
    # )
