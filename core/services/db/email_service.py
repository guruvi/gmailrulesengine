""" This module contains the email service methods. """


import logging

from core.pydantic_models import EmailData
from gmail_rules_engine.tables import Email
from piccolo.columns.combination import And, Or


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
    Email(
        email_id=email.reference_id,
        gmail_message_id=email.gmail_message_id,
        from_address=email.from_address,
        to_address=email.to_address,
        date_received=email.date_received,
        subject=email.subject,
    ).save().run_sync()
    LOGGER.info("Email record has been successfully created in the database.")
    return Email
