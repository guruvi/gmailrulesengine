""" This library contains different actions to be done on the messages. """


from core.services.gmail.client import batch_update_labels


def execute_gmail_actions(
    user_id: str, message_ids: list[str], actions_config: dict
) -> None:
    """
    Invoke the Google API to update labels after converting the actions to labels.

    :param user_id: The user id.
    :type user_id: str

    :param message_ids: A list of message ids.
    :type message_ids: list[str]

    :param actions_config: A dictionary containing the configuration for actions.
    :type actions_config: dict
    """
    add_labels, remove_labels = convert_actions_to_labels(actions_config)
    batch_update_labels(
        user_id=user_id,
        message_ids=message_ids,
        add_labels=add_labels,
        remove_labels=remove_labels,
    )


def convert_actions_to_labels(actions_config: dict) -> tuple[list[str], list[str]]:
    """
    Convert actions to labels.

    :param actions_config: A dictionary containing the actions_config to be converted.
    :type actions_config: dict

    :return: A tuple containing two lists - the labels to be added and the labels to be removed.
    :rtype: tuple[list[str], list[str]]
    """
    move_action: dict = actions_config.get("actions", {})
    add_labels: list[str] = []
    remove_labels: list[str] = []

    action: str | None = move_action.get("move")
    mark_actions: list[str] = move_action.get("mark", [])

    add_labels.append(action) if action else None
    for mark_action in mark_actions:
        match mark_action:
            case "UNREAD":
                add_labels.append("UNREAD")
            case "READ":
                remove_labels.append("UNREAD")
            case "IMPORTANT":
                add_labels.append("IMPORTANT")
            case "UNIMPORTANT":
                remove_labels.append("IMPORTANT")
    return add_labels, remove_labels
