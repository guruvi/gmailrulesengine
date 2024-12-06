""" This module fetches the email from Gmail API and stores it in the database. """


import datetime
import logging
from typing import Any

from core.pydantic_models import EmailData
from core.services.db.email_service import create_email
from core.services.gmail.client import get_email_message, list_email

LOGGER: logging.Logger = logging.getLogger(name=__name__)


def parse_datetime_email(value: str) -> datetime.datetime:
    """Parse the datetime string to datetime object.

    :param date: Date string
    :type date: str

    :returns: Datetime object
    :rtype: datetime.datetime
    """
    for fmt in ["%a, %d %b %Y %H:%M:%S %z", "%d %b %Y %H:%M:%S %z"]:
        try:
            return datetime.datetime.strptime(value.split(" (")[0], fmt)
        except ValueError:
            pass


# Mapping header names to actions
HEADER_HANDLERS: dict[str, Any] = {
    "From": lambda fields, value: fields.update({"from_address": value}),
    "To": lambda fields, value: fields.update({"to_address": value}),
    "Subject": lambda fields, value: fields.update({"subject": value}),
    "Date": lambda fields, value: fields.update(
        {"date_received": parse_datetime_email(value)}
    ),
}


def process(*, user_id: str):
    """
    Fetch and store email from Gmail API.

    :param user_id: User's email id
    :type user_id: str
    """
    LOGGER.info("Fetching email from Gmail API")
    email_list = list_email(user_id=user_id)
    for email in email_list["messages"]:
        email_message = get_email_message(user_id=user_id, message_id=email["id"])
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
    LOGGER.info("Email has been successfully fetched and stored in the database.")
