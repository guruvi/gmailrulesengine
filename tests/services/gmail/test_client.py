from typing import Any
from unittest import mock
import pytest

from core.services.gmail.client import get_access_token, get_email_message, list_email

pytestmark = pytest.mark.gmail_client


def test_should_raise_value_error_when_the_auth_scopes_list_is_empty():
    with pytest.raises(ValueError, match="Scopes list cannot be empty"):
        get_access_token(scopes=[])


def test_should_raise_file_not_found_error_when_credentials_file_does_not_exists():
    test_scopes = ["https://www.googleapis.com/auth/drive.readonly"]

    with mock.patch("os.path.exists", return_value=False), pytest.raises(
        FileNotFoundError, match="Credentials file not found"
    ):
        get_access_token(scopes=test_scopes)


def test_get_access_token():
    with mock.patch(
        "google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file"
    ) as mock_flow:
        mock_credentials = {
            "token": "token",
            "refresh_token": "refresh_token",
            "token_uri": "https://oauth2.googleapis.com/token",
            "client_id": "client_id.apps.googleusercontent.com",
            "client_secret": "client_secret",
            "scopes": ["https://mail.google.com/"],
            "universe_domain": "googleapis.com",
            "account": "",
            "expiry": "2024-11-30T18:02:43.682924Z",
        }
        mock_flow.return_value.run_local_server.return_value = mock_credentials
        result = get_access_token(scopes=["scope1", "scope2"])

        assert result == mock_credentials
        mock_flow.assert_called_once_with(
            "/Users/guruvi/Downloads/credentials.json", ["scope1", "scope2"]
        )
        mock_flow.return_value.run_local_server.assert_called_once_with(port=0)


def test_should_raise_exception():
    with mock.patch(
        "google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file"
    ) as mock_flow:
        mock_flow.return_value.run_local_server.side_effect = Exception(
            "Authentication failed"
        )
        with pytest.raises(Exception, match="Authentication failed"):
            get_access_token(scopes=["scope1", "scope2"])


@mock.patch("core.services.gmail.client.get_access_token")
@mock.patch("core.services.gmail.client.build")
def test_should_list_all_emails(mock_build_google_service, mock_credentials):
    mock_credentials.return_value = {
        "token": "token",
        "refresh_token": "refresh_token",
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_id": "client_id.apps.googleusercontent.com",
        "client_secret": "client_secret",
        "scopes": ["https://mail.google.com/"],
        "universe_domain": "googleapis.com",
        "account": "",
        "expiry": "2024-11-30T18:02:43.682924Z",
    }
    service = mock.MagicMock()
    mock_build_google_service.return_value = service
    service.users.return_value.messages.return_value.list.return_value.execute.return_value = [
        {"id": "19380f65a0cd3791", "threadId": "19380664d0cd9a9b"},
        {"id": "19380f4b5b231e0e", "threadId": "19380f4b5b231e0e"},
    ]
    response = list_email(user_id="test_user_id")

    mock_build_google_service.assert_called_once_with(
        "gmail",
        "v1",
        credentials={
            "token": "token",
            "refresh_token": "refresh_token",
            "token_uri": "https://oauth2.googleapis.com/token",
            "client_id": "client_id.apps.googleusercontent.com",
            "client_secret": "client_secret",
            "scopes": ["https://mail.google.com/"],
            "universe_domain": "googleapis.com",
            "account": "",
            "expiry": "2024-11-30T18:02:43.682924Z",
        },
    )
    # Add assertion for list message to be correctly invoked
    assert response == [
        {"id": "19380f65a0cd3791", "threadId": "19380664d0cd9a9b"},
        {"id": "19380f4b5b231e0e", "threadId": "19380f4b5b231e0e"},
    ]


# TODO: Add test case for list_email to raise exception
# TODO: Add test case for get message to raise exception


@mock.patch("core.services.gmail.client.get_access_token")
@mock.patch("core.services.gmail.client.build")
def test_should_get_message_based_on_message_id(
    mock_build_google_service, mock_credentials
):
    mock_credentials.return_value = {
        "token": "token",
        "refresh_token": "refresh_token",
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_id": "client_id.apps.googleusercontent.com",
        "client_secret": "client_secret",
        "scopes": ["https://mail.google.com/"],
        "universe_domain": "googleapis.com",
        "account": "",
        "expiry": "2024-11-30T18:02:43.682924Z",
    }

    get_message_response: dict[str, Any] = {
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
                    "value": "by 2002:a05:640c:1501:b0:219:8a79:a0ea with SMTP id n1csp1169483eir;        Sat, 30 Nov 2024 22:44:09 -0800 (PST)",
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
    service = mock.MagicMock()
    mock_build_google_service.return_value = service
    service.users.return_value.messages.return_value.get.return_value.execute.return_value = (
        get_message_response
    )

    response = get_email_message(user_id="test_user_id", message_id="19380f65a0cd3791")

    mock_build_google_service.assert_called_once_with(
        "gmail",
        "v1",
        credentials={
            "token": "token",
            "refresh_token": "refresh_token",
            "token_uri": "https://oauth2.googleapis.com/token",
            "client_id": "client_id.apps.googleusercontent.com",
            "client_secret": "client_secret",
            "scopes": ["https://mail.google.com/"],
            "universe_domain": "googleapis.com",
            "account": "",
            "expiry": "2024-11-30T18:02:43.682924Z",
        },
    )
    # Add assertion for get message to be correctly invoked
    assert response == get_message_response
