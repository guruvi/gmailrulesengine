""" This module fetches the email from Gmail API and stores it in the database. """


import datetime
import logging
from typing import Any

from core.pydantic_models import EmailData
from core.services.db.email_service import create_email
from core.services.gmail.client import get_email_message, list_email

LOGGER: logging.Logger = logging.getLogger(name=__name__)


def process(*, user_id: str, page_size: int = 10, no_of_pages: int = 10) -> None:
    """
    Fetch and store email from Gmail API.

    :param user_id: User's email id
    :type user_id: str

    :param page_size: Page size
    :type page_size: int

    :param no_of_pages: Number of pages
    :type no_of_pages: int

    :returns: None
    :rtype: None
    """
    LOGGER.info("Fetching email from Gmail API")
    email_list_iter = list_email_batch(user_id=user_id, page_size=page_size, no_of_pages=no_of_pages)
    for email_list in email_list_iter:
        for email in email_list:
            email_message = get_email_message(user_id=user_id, message_id=email["id"])
            print(email["id"])
            # Process email headers
            email_data_fields: dict[str, Any] = {}
            for header in email_message["payload"]["headers"]:
                name: str = header.get("name")
                value: Any = header.get("value")
                if name in HEADER_HANDLERS:
                    HEADER_HANDLERS[name](email_data_fields, value)
            email_data_fields.update({"gmail_message_id": email_message["id"]})
            email_data = EmailData(**email_data_fields)
            create_email(email=email_data)
            LOGGER.info(f"Email {email_message['id']} stored successfully.")


def list_email_batch(*, user_id: str, page_size: int = 10, no_of_pages: int = 10):
    """ 
    This email fetches the email list in batches.
    
    :param user_id: User id
    :type user_id: str

    :param page_size: Page size
    :type page_size: int

    :param no_of_pages: Number of pages
    :type no_of_pages: int
    """
    email_list = list_email(user_id=user_id, page_size=page_size)
    yield email_list["messages"]
    for x in range(no_of_pages - 1):
        next_page_token = email_list.get("nextPageToken")
        if next_page_token:
            email_list = list_email(user_id=user_id, page_size=page_size, page_token=next_page_token)
            yield email_list["messages"]
        else:
            break


# Mapping header names to actions
HEADER_HANDLERS: dict[str, Any] = {
    "From": lambda fields, value: fields.update({"from_address": value}),
    "To": lambda fields, value: fields.update({"to_address": value}),
    "Subject": lambda fields, value: fields.update({"subject": value}),
    "Date": lambda fields, value: fields.update(
        {"date_received": parse_datetime_email(value)}
    ),
}


def parse_datetime_email(value: str) -> datetime.datetime:
    """Parse the datetime string to datetime object.

    :param date: Date string
    :type date: str

    :returns: Datetime object
    :rtype: datetime.datetime
    """
    for fmt in ["%a, %d %b %Y %H:%M:%S %z", "%d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S", "%a, %d %b %Y %H:%M:%S %Z"]:
        try:
            return datetime.datetime.strptime(value.split(" (")[0], fmt)
        except ValueError:
            pass
