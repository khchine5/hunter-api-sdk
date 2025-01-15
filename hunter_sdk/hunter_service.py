import logging
import requests
from .storage import InMemoryStorage

logger = logging.getLogger(__name__)


class HunterService:
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

    def verify_email(self, email: str):
        """Validate an email address and store the result."""
        # Check if email is already in storage_service
        cached_result = self.storage_service.get(email)
        if cached_result:
            logger.debug(
                f"Email {email} found in storage_service. Returning cached result."
            )
            return cached_result

        url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={self.api_key}"
        headers = {"Accept": "application/json"}

        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, headers=headers)
                logger.debug(
                    f"Requesting email validation for {email}. "
                    f"Status: {response.status_code}"
                )

                if response.status_code == 202:
                    logger.debug(
                        f"Email {email} is still being processed. "
                        f"Retrying in {self.retry_delay} seconds (Attempt {attempt + 1}/{self.max_retries})."
                    )
                    import time

                    time.sleep(self.retry_delay)
                    continue

                if response.status_code == 200:
                    data = response.json()
                    self.storage_service.set(email, data["data"])
                    logger.debug(f"Validation successful for {email}.")
                    return data["data"]

                logger.error(f"Error validating email {email}: {response.status_code}")
                return None

            except Exception as e:
                logger.error(f"An error occurred: {e}")

        logger.warning(f"Max retries reached for {email}. Returning None.")
        return None
