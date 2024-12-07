import datetime
import uuid
import pytest

from core.pydantic_models import EmailData
from core.services.db.email_service import create_email, filter_emails
from gmail_rules_engine.tables import Email

pytestmark = pytest.mark.email_db_service


def test_should_insert_email_into_db():
    email_data: EmailData = EmailData(
        reference_id=uuid.uuid4(),
        gmail_message_id=str(uuid.uuid4()),
        from_address="abc@gmail.com",
        to_address="def@gmail.com",
        date_received=datetime.datetime.now(tz=datetime.timezone.utc),
        subject="Test Email",
    )
    create_email(email=email_data)

    email = Email.objects().get(Email.email_id == email_data.reference_id).run_sync()
    assert email.gmail_message_id == email_data.gmail_message_id
    assert email.from_address == email_data.from_address
    assert email.to_address == email_data.to_address
    assert email.date_received == email_data.date_received
    assert email.subject == email_data.subject


def test_email_query_filter():
    email_data: EmailData = EmailData(
        reference_id=uuid.uuid4(),
        gmail_message_id=str(uuid.uuid4()),
        from_address="abcdef@gmail.com",
        to_address="def@gmail.com",
        date_received=datetime.datetime.now(tz=datetime.timezone.utc),
        subject="Test Email",
    )
    create_email(email=email_data)
    # Filter condition
    query = Email.from_address == "abcdef@gmail.com"
    result_email = filter_emails(query=query)[0]

    assert result_email.gmail_message_id == email_data.gmail_message_id
    assert result_email.from_address == email_data.from_address
    assert result_email.to_address == email_data.to_address
    assert result_email.date_received == email_data.date_received
    assert result_email.subject == email_data.subject
