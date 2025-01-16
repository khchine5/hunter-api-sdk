import pytest
import requests as http_requests
import responses

from hunter_sdk.hunter_service import HunterService
from hunter_sdk.storage import InMemoryStorage


@pytest.fixture
def mock_storage() -> InMemoryStorage:
    return InMemoryStorage()


@pytest.fixture
def mock_hunter_service(mock_storage: InMemoryStorage) -> HunterService:
    return HunterService(api_key="mock_api_key", storage_service=mock_storage)


class TestHunterServiceCaching:
    @responses.activate
    def test_uses_cache(self, mock_hunter_service: HunterService) -> None:
        email = "test@example.com"
        cached_response = {"email": email, "status": "valid"}
        mock_hunter_service.storage_service.set(email, cached_response)

        response = mock_hunter_service.verify_email(email)

        assert response == cached_response

    @responses.activate
    def test_stores_result(self, mock_hunter_service: HunterService) -> None:
        email = "store@example.com"
        api_response = {"data": {"email": email, "status": "valid"}}
        responses.add(
            responses.GET,
            f"https://api.hunter.io/v2/email-verifier?email={email}&api_key=mock_api_key",
            json=api_response,
            status=http_requests.codes.all_ok,
        )

        response = mock_hunter_service.verify_email(email)

        assert response == api_response["data"]
        assert mock_hunter_service.storage_service.get(email) == api_response["data"]


class TestHunterServiceHTTP:
    @responses.activate
    def test_makes_request(self, mock_hunter_service: HunterService) -> None:
        email = "http@example.com"
        api_response = {"data": {"email": email, "status": "valid"}}
        responses.add(
            responses.GET,
            f"https://api.hunter.io/v2/email-verifier?email={email}&api_key=mock_api_key",
            json=api_response,
            status=http_requests.codes.all_ok,
        )

        response = mock_hunter_service.verify_email(email)

        assert response == api_response["data"]
        assert len(responses.calls) == 1

    @responses.activate
    def test_handles_error(self, mock_hunter_service: HunterService) -> None:
        email = "error@example.com"
        responses.add(
            responses.GET,
            f"https://api.hunter.io/v2/email-verifier?email={email}&api_key=mock_api_key",
            status=http_requests.codes.bad_request,
        )

        response = mock_hunter_service.verify_email(email)

        assert response is None
        assert len(responses.calls) == 5  # Max retries reached


class TestHunterServiceRetries:
    @responses.activate
    def test_retries_on_accepted(self, mock_hunter_service: HunterService) -> None:
        email = "retry@example.com"
        api_response = {"data": {"email": email, "status": "valid"}}
        responses.add(
            responses.GET,
            f"https://api.hunter.io/v2/email-verifier?email={email}&api_key=mock_api_key",
            status=http_requests.codes.accepted,
        )
        responses.add(
            responses.GET,
            f"https://api.hunter.io/v2/email-verifier?email={email}&api_key=mock_api_key",
            json=api_response,
            status=http_requests.codes.all_ok,
        )

        response = mock_hunter_service.verify_email(email)

        assert response == api_response["data"]
        assert len(responses.calls) == 2
