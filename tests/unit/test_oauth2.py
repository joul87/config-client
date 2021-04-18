import pytest

from config import http
from config.auth import OAuth2
from config.exceptions import RequestFailedException, RequestTokenException
from tests import conftest


class TestOAuth2:
    @pytest.fixture
    def oauth2(self):
        return OAuth2(
            access_token_uri="https://p-spring-cloud-services.uaa.sys.example.com/oauth/token",
            client_id="p-config-server-example-client-id",
            client_secret="EXAMPLE_SECRET",
        )

    def test_token(self, oauth2):
        assert oauth2.token == ""

    def test_configure(self, oauth2, monkeypatch):
        monkeypatch.setattr(http, "post", conftest.response_mock_success)
        oauth2.configure()
        assert oauth2.token is not None

    def test_configure_failed(self, oauth2, monkeypatch):
        monkeypatch.setattr(http, "post", conftest.http_error)
        with pytest.raises(RequestTokenException):
            oauth2.configure()

    def test_configure_request_failed(self, oauth2, monkeypatch):
        monkeypatch.setattr(http, "post", conftest.missing_schema_error)
        with pytest.raises(RequestFailedException):
            oauth2.configure()

    def test_authorization_header(self, oauth2, monkeypatch):
        monkeypatch.setattr(http, "post", conftest.response_mock_success)
        oauth2.configure()
        assert isinstance(oauth2.authorization_header, dict)
