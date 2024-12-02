""" This file contains the Pydantic model definitions. """


import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel


class EmailData(BaseModel):
    """This class contains the Pydantic model for the email data."""

    reference_id: UUID = uuid4()
    gmail_message_id: str
    from_address: str
    to_address: str
    date_received: datetime.datetime
    subject: str
