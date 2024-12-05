import datetime
import uuid
import pytest

from core.pydantic_models import EmailData
from core.services.db.email_service import create_email
from gmail_rules_engine.tables import Email

pytestmark = pytest.mark.email_db_service


def test_should_insert_email_into_db():
    email_data: EmailData = EmailData(
        reference_id=uuid.uuid4(),
        gmail_message_id="123",
        from_address="abc@gmail.com",
        to_address="def@gmail.com",
        date_received=datetime.datetime.now(tz=datetime.timezone.utc),
        subject="Test Email",
    )
    create_email(email=email_data)

    email = Email.objects().get(Email.email_id == email_data.reference_id).run_sync()
    assert email.email_id == email_data.reference_id
    assert email.gmail_message_id == email_data.gmail_message_id
    assert email.from_address == email_data.from_address
    assert email.to_address == email_data.to_address
    assert email.date_received == email_data.date_received
    assert email.subject == email_data.subject
