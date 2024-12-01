"""This module contains different client methods for accessing Gmail APIs."""


import os
from typing import Any, Final
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build, Resource
import logging

LOGGER: Final[logging.Logger] = logging.getLogger(name=__name__)


def get_access_token(*, scopes: list) -> Credentials:
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

    credentials_path = "/Users/guruvi/Downloads/credentials.json"
    if not os.path.exists(credentials_path):
        raise FileNotFoundError("Credentials file not found")

    try:
        flow = InstalledAppFlow.from_client_secrets_file(credentials_path, scopes)
        credentials: Credentials = flow.run_local_server(port=0)
        LOGGER.info("Credentials has been successfully fetched from the server.")
        return credentials
    except Exception as e:
        raise e


def list_email(*, user_id: str) -> dict[str, Any]:
    """
    List the user's Gmail labels.

    :param user_id: User id
    :type user_id: str
    """
    LOGGER.info("Invoking Gmail messages list API")
    credentials = get_access_token(scopes=["https://mail.google.com/"])
    service: Resource = build("gmail", "v1", credentials=credentials)
    results = (
        service.users()
        .messages()
        .list(userId=user_id, maxResults=10, labelIds=["INBOX"])
        .execute()
    )
    LOGGER.info("Gmail list message API response successful.")
    return results


def list_email(*, user_id: str) -> dict[str, Any]:
    """
    List the user's Gmail labels.

    :param user_id: User id
    :type user_id: str
    """
    LOGGER.info("Invoking Gmail messages list API")
    credentials = get_access_token(scopes=["https://mail.google.com/"])
    service: Resource = build("gmail", "v1", credentials=credentials)
    results = service.users().messages().list(userId=user_id).execute()
    LOGGER.info("Gmail list message API response successful.")
    return results


def get_email_message(*, user_id: str, message_id: str) -> dict[str, Any]:
    """
    Get the user's Gmail labels.

    :param user_id: User id
    :type user_id: str
    """
    LOGGER.info("Invoking Gmail messages get API")
    credentials = get_access_token(scopes=["https://mail.google.com/"])
    service: Resource = build("gmail", "v1", credentials=credentials)
    results = service.users().messages().get(userId=user_id, id=message_id).execute()
    LOGGER.info("Gmail get message API response successful.")
    return results
