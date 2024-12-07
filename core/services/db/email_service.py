""" This module contains the email service methods. """


import logging
import sqlite3
import uuid

from core.pydantic_models import EmailData
from gmail_rules_engine.tables import Email
from piccolo.columns.combination import And, Or, Where


LOGGER: logging.Logger = logging.getLogger(name=__name__)


def create_email(*, email: EmailData) -> Email:
    """
    Create an email record in the database.

    :param email: Email data
    :type email EmailData

    :return: Email
    :rtype: Email
    """
    LOGGER.info("Creating email record in the database")
    try:
        Email(
            email_id=str(uuid.uuid4()),
            gmail_message_id=email.gmail_message_id,
            from_address=email.from_address,
            to_address=email.to_address,
            date_received=email.date_received,
            subject=email.subject,
        ).save().run_sync()
    except sqlite3.IntegrityError as ex:
        pass

    LOGGER.info("Email record has been successfully created in the database.")
    return Email


def filter_emails(*, query: Where | And | Or) -> list[Email]:
    """
    Query emails from the database.

    :param query: Query string
    :type query:  Where | And | Or

    :return: List of emails
    :rtype: list[Email]
    """
    LOGGER.info("Querying emails from the database")
    emails: list[Email] = Email.objects().where(query).run_sync()
    LOGGER.info("Emails have been successfully queried from the database.")
    return emails
