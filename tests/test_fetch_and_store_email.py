import datetime
from unittest import mock
import pytest

from core.fetch_and_store_email import process
from gmail_rules_engine.tables import Email

pytestmark = pytest.mark.fetch_and_store_email


@mock.patch("core.fetch_and_store_email.list_email")
@mock.patch("core.fetch_and_store_email.get_email_message")
def test_should_fetch_and_store_email(get_email_message_mock, list_email_mock):
    list_email_mock.return_value = {
        "messages": [{"id": "19380f65a0cd3791", "threadId": "19380664d0cd9a9b"}]
    }
    get_email_message_mock.return_value = {
        "id": "19380f65a0cd3791",
        "threadId": "19380664d0cd9a9b",
        "labelIds": ["CATEGORY_PERSONAL", "INBOX"],
        "snippet": "Dear Sir/Madam,",
        "payload": {
            "partId": "",
            "mimeType": "multipart/mixed",
            "filename": "",
            "headers": [
                {"name": "Delivered-To", "value": "abcde@gmail.com"},
                {
                    "name": "Received",
                    "value": "by 2002:a05:640c:1501:b0:219:8a79:a0ea with SMTP id n1csp2837164eir;        Tue, 3 Dec 2024 01:47:41 -0800 (PST)",
                },
                {"name": "Date", "value": "Sun, 1 Dec 2024 11:36:27 +0530 (IST)"},
                {"name": "From", "value": "kblalerts@ktkbank.in"},
                {"name": "To", "value": "abcde@gmail.com"},
                {
                    "name": "Subject",
                    "value": "****** BANK- Transaction EMAIL Alert ******",
                },
                {"name": "Mime-Version", "value": "1.0"},
            ],
            "body": {"size": 0},
            "parts": [],
        },
        "sizeEstimate": 6144,
        "historyId": "9474857",
        "internalDate": "1733033187000",
    }

    process(user_id="abcd@gmail.com")

    email: Email = (
        Email.objects().get(Email.gmail_message_id == "19380f65a0cd3791").run_sync()
    )
    assert email.gmail_message_id == "19380f65a0cd3791"
    assert email.from_address == "kblalerts@ktkbank.in"
    assert email.to_address == "abcde@gmail.com"
    assert email.date_received == datetime.datetime(
        year=2024,
        month=12,
        day=1,
        hour=6,
        minute=6,
        second=27,
        tzinfo=datetime.timezone.utc,
    )
    assert email.subject == "****** BANK- Transaction EMAIL Alert ******"
