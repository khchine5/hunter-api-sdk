import logging
from typing import Optional

import requests as http_requests

logger = logging.getLogger(__name__)


def _build_verification_url(api_key: str, email: str) -> str:
    return f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={api_key}"


def _send_request(url: str, headers: dict) -> Optional[http_requests.Response]:
    try:
        return http_requests.get(url, headers=headers)
    except http_requests.RequestException as exc:
        logger.error("An error occurred while making the request: %s", exc)
    return None


def _handle_error_response(email: str, response: http_requests.Response) -> None:
    logger.error(
        "Error validating email %s: Status code %d, Response: %s",
        email,
        response.status_code,
        response.text,
    )
