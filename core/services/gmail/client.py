"""This module contains different client methods for accessing Gmail APIs."""


from functools import cache
import os
from typing import Any, Final
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build, Resource
import logging

LOGGER: Final[logging.Logger] = logging.getLogger(name=__name__)


@cache
def get_access_token(*, scopes: tuple) -> Credentials:
    """
    Get the access token from the credentials.json file.

    :param scopes: The authorization scope
    :type scopes: list

    :returns oauth2 credentials
    :rtype google.oauth2.credentials.Credentials

    :raises ValueError: If scopes list is empty
    :raises FileNotFoundError: If credentials file is missing
    """
    LOGGER.info("Invoking Google auth API to get access token")
    if not scopes:
        raise ValueError("Scopes list cannot be empty")

    credentials_path = os.getenv("PATH_TO_CREDENTIALS_JSON")
    if not os.path.exists(credentials_path):
        raise FileNotFoundError("Credentials file not found")

    try:
        flow = InstalledAppFlow.from_client_secrets_file(credentials_path, list(scopes))
        credentials: Credentials = flow.run_local_server(port=0)
        LOGGER.info("Credentials has been successfully fetched from the server.")
        return credentials
    except Exception as e:
        raise e


def list_email(*, user_id: str, page_size: int=100, **kwargs: Any) -> dict[str, Any]:
    """
    List the user's Gmail labels.

    :param user_id: User id
    :type user_id: str

    :param page_size: Page size
    :type page_size: int

    :param kwargs: Keyword arguments
    :type kwargs: Any

    :returns: Email list messages response
    :rtype: dict
    """
    LOGGER.info("Invoking Gmail messages list API")
    credentials = get_access_token(scopes=("https://mail.google.com/",))

    # Set the query parameters
    params: dict[str, Any] = {
        "userId": user_id,
        "maxResults": page_size,
    }
    if kwargs.get("page_token"):
        params["pageToken"] = kwargs.get("page_token")

    if not credentials.valid:
        credentials = get_access_token(scopes=("https://mail.google.com/",))

    service: Resource = build("gmail", "v1", credentials=credentials)
    results = (
        service.users()
        .messages()
        .list(**params)
        .execute()
    )
    LOGGER.info("Gmail list message API response successful.")
    return results


def get_email_message(*, user_id: str, message_id: str) -> dict[str, Any]:
    """
    Get the user's Gmail labels.

    :param user_id: User id
    :type user_id: str
    """
    LOGGER.info("Invoking Gmail messages get API")
    credentials = get_access_token(scopes=("https://mail.google.com/",))
    if not credentials.valid:
        credentials = get_access_token(scopes=("https://mail.google.com/",))
    credentials = get_access_token(scopes=("https://mail.google.com/",))
    service: Resource = build("gmail", "v1", credentials=credentials)
    results = service.users().messages().get(userId=user_id, id=message_id).execute()
    LOGGER.info("Gmail get message API response successful.")
    return results


def batch_update_labels(
    *,
    user_id: str,
    message_ids: list[str],
    add_labels: list[str],
    remove_labels: list[str],
) -> dict[str, Any]:
    """
    Move the message from one label to another.

    :param source_label: Source label
    :type source_label: str

    :param destination_label: Destination label
    :type destination_label: str
    """
    LOGGER.info("Invoking Gmail messages move API")
    credentials = get_access_token(scopes=("https://mail.google.com/",))
    if not credentials.valid:
        credentials = get_access_token(scopes=("https://mail.google.com/",))
    service: Resource = build("gmail", "v1", credentials=credentials)
    results = (
        service.users()
        .messages()
        .batchModify(
            userId=user_id,
            body={
                "ids": message_ids,
                "addLabelIds": add_labels,
                "removeLabelIds": remove_labels,
            },
        )
        .execute()
    )
    LOGGER.info("Gmail move message API response successful.")
    return results
