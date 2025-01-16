from unittest.mock import patch

import pytest
import responses

from hunter_sdk.hunter_service import HunterService
from hunter_sdk.storage import InMemoryStorage


@pytest.fixture
def mock_storage():
    return InMemoryStorage()


@pytest.fixture
def mock_hunter_service(mock_storage):
    return HunterService(api_key="mock_api_key", storage_service=mock_storage)


@responses.activate
def test_verify_email_uses_cache(mock_hunter_service):
    """Test that verify_email uses the cached result if available."""
    email = "test@example.com"
    cached_data = {"email": email, "status": "valid"}

    # Store the data in the mock storage
    mock_hunter_service.storage_service.set(email, cached_data)

    # No HTTP response is mocked because the cache should be used
    result = mock_hunter_service.verify_email(email)

    # Ensure the result is from the cache
    assert result == cached_data


@responses.activate
def test_verify_email_http_request(mock_hunter_service):
    """Test that verify_email makes an HTTP request if email is not in cache."""
    email = "test@example.com"
    response_data = {"data": {"email": email, "status": "valid"}}

    # Mock the HTTP response
    responses.add(
        responses.GET,
        f"https://api.hunter.io/v2/email-verifier?email={email}&api_key=mock_api_key",
        json=response_data,
        status=200,
    )

    result = mock_hunter_service.verify_email(email)

    # Ensure the result is from the HTTP response
    assert result == response_data["data"]

    # Verify that the request was made
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == (
        f"https://api.hunter.io/v2/email-verifier?email={email}&api_key=mock_api_key"
    )


@responses.activate
def test_verify_email_uses_cache_without_request(mock_hunter_service):
    """Test that verify_email uses the cached result and skips the HTTP request."""
    email = "cached@example.com"
    cached_data = {"email": email, "status": "valid"}

    # Store the data in the mock storage
    mock_hunter_service.storage_service.set(email, cached_data)

    # No HTTP response is mocked because the cache should be used
    result = mock_hunter_service.verify_email(email)

    # Ensure the result is from the cache
    assert result == cached_data

    # Ensure no HTTP request was made
    assert len(responses.calls) == 0


@responses.activate
def test_verify_email_retries_on_202(mock_hunter_service):
    """Test that verify_email retries when receiving a 202 status code."""
    email = "retry@example.com"
    response_data = {"data": {"email": email, "status": "valid"}}

    # Mock a 202 response for the first call and a 200 response for the second call
    responses.add(
        responses.GET,
        f"https://api.hunter.io/v2/email-verifier?email={email}&api_key=mock_api_key",
        status=202,
    )
    responses.add(
        responses.GET,
        f"https://api.hunter.io/v2/email-verifier?email={email}&api_key=mock_api_key",
        json=response_data,
        status=200,
    )

    result = mock_hunter_service.verify_email(email)

    # Ensure the result is from the successful response
    assert result == response_data["data"]

    # Ensure two HTTP requests were made (one retry)
    assert len(responses.calls) == 2


@responses.activate
def test_verify_email_handles_http_error(mock_hunter_service):
    """Test that verify_email handles non-200/202 status codes gracefully."""
    email = "error@example.com"

    # Mock a 400 Bad Request response
    responses.add(
        responses.GET,
        f"https://api.hunter.io/v2/email-verifier?email={email}&api_key=mock_api_key",
        status=400,
    )

    result = mock_hunter_service.verify_email(email)

    # Ensure the result is None for an error response
    assert result is None

    # Ensure one HTTP request was made
    assert len(responses.calls) == 1


@responses.activate
def test_verify_email_handles_rate_limit(mock_hunter_service):
    """Test that verify_email handles rate-limiting gracefully."""
    email = "rate_limit@example.com"

    # Mock a 429 Too Many Requests response
    responses.add(
        responses.GET,
        f"https://api.hunter.io/v2/email-verifier?email={email}&api_key=mock_api_key",
        status=429,
    )

    result = mock_hunter_service.verify_email(email)

    # Ensure the result is None for a rate-limiting response
    assert result is None

    # Ensure one HTTP request was made
    assert len(responses.calls) == 1


@responses.activate
def test_verify_email_handles_exception(mock_hunter_service):
    """Test that verify_email handles unexpected exceptions gracefully."""
    email = "exception@example.com"

    # Simulate an exception during the request
    with patch("requests.get", side_effect=Exception("Connection error")):
        result = mock_hunter_service.verify_email(email)

        # Ensure the result is None for an exception
        assert result is None


@responses.activate
def test_verify_email_stores_result(mock_hunter_service):
    """Test that verify_email stores the result in storage after validation."""
    email = "store@example.com"
    response_data = {"data": {"email": email, "status": "valid"}}

    # Mock a successful 200 response
    responses.add(
        responses.GET,
        f"https://api.hunter.io/v2/email-verifier?email={email}&api_key=mock_api_key",
        json=response_data,
        status=200,
    )

    result = mock_hunter_service.verify_email(email)

    # Ensure the result is from the HTTP response
    assert result == response_data["data"]

    # Ensure the data is stored in storage
    assert mock_hunter_service.storage_service.get(email) == response_data["data"]
