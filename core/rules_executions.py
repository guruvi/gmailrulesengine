""" This method filters the messages based on the rules, apply actions and update the labels. """


from core.rules_engine.apply_rules import construct_query
from core.rules_engine.execute_actions import execute_gmail_actions
from core.services.db.email_service import filter_emails
from gmail_rules_engine.tables import Email
from piccolo.columns.combination import And, Or, Where


def execute(*, user_id: str, config_dict: dict) -> None:
    """
    Executes the actions based on the rules engine results.

    :param user_id: The user id.
    :type user_id: str

    :param config_dict: The configuration dictionary.
    :type config_dict: dict
    """
    filter_query: And | Or | Where = construct_query(config_dict)
    # Get the messages based on the filter query
    messages: list[Email] = filter_emails(query=filter_query)
    # Apply actions on the messages
    execute_gmail_actions(
        user_id=user_id,
        message_ids=[message.gmail_message_id for message in messages],
        actions_config=config_dict["actions"],
    )
