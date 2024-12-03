""" This model contains classes for the database tables"""


from piccolo.table import Table
from piccolo.columns import UUID, Text, Timestamptz


class Email(Table):
    """Describes attributes and constraints on account of a customer."""

    email_id: UUID = UUID(null=False, index=True)
    gmail_message_id: Text = Text(null=False, index=True, unique=True)
    from_address: Text = Text(null=False, index=True)
    to_address: Text = Text(null=False, index=True)
    date_received: Timestamptz = Timestamptz(null=False, index=True)
    subject: Text = Text(null=False, index=True)
