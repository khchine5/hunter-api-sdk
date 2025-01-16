import logging
import time
from typing import Optional

import requests as http_requests

from hunter_sdk.requests_operations import (
    _build_verification_url,
    _handle_error_response,
    _send_request,
)
from hunter_sdk.storage import InMemoryStorage

logger = logging.getLogger(__name__)


class HunterService:
    """Service for interacting with the Hunter.io API."""

    def __init__(
        self,
        api_key: str,
        storage_service: InMemoryStorage,
        max_retries: int = 5,
        retry_delay: int = 5,
    ):
        self.api_key = api_key
        self.storage_service = storage_service
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def verify_email(self, email: str) -> Optional[dict]:
        cached_result = self._get_cached_result(email)
        if cached_result:
            return cached_result

        return self._perform_email_validation(email)

    def _get_cached_result(self, email: str) -> Optional[dict]:
        cached_result = self.storage_service.get(email)
        if cached_result:
            logger.debug("Cached result found for email: %s", email)
        return cached_result

    def _process_response(
        self, email: str, response: http_requests.Response, attempt: int
    ) -> Optional[dict]:
        """Process the API response and handle statuses."""
        if response.status_code == http_requests.codes.all_ok:
            return self._handle_successful_response(email, response)

        if response.status_code == http_requests.codes.accepted:
            self._handle_processing_response(email, attempt)
            return None

        _handle_error_response(email, response)
        return None

    def _perform_email_validation(self, email: str) -> Optional[dict]:
        """Perform email validation by making API requests."""
        url = _build_verification_url(email=email, api_key=self.api_key)
        headers = {"Accept": "application/json"}

        for attempt in range(1, self.max_retries + 1):
            response = _send_request(url, headers)
            if response is None:
                continue

            validation_data = self._process_response(email, response, attempt)
            if validation_data:
                return validation_data

        logger.warning("Max retries reached for email: %s", email)
        return None

    def _handle_successful_response(
        self, email: str, response: http_requests.Response
    ) -> dict:
        response_data = response.json()
        self.storage_service.set(email, response_data["data"])
        logger.debug("Validation successful for email: %s", email)
        return response_data["data"]

    def _handle_processing_response(self, email: str, attempt: int) -> None:
        logger.debug(
            "Email %s is still being processed. Retrying in %d seconds (Attempt %d/%d).",
            email,
            self.retry_delay,
            attempt,
            self.max_retries,
        )
        time.sleep(self.retry_delay)
