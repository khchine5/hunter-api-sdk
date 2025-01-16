import json
import logging

logger = logging.getLogger(__name__)


class InMemoryStorage:
    """
    In-memory storage implementation.
    """

    def __init__(self, storage_path: str = "data.json"):
        """
        Initialize an empty storage and load existing data if available.
        """
        self._storage: dict[str, dict] = {}
        self._storage_path = storage_path
        self.load()

    def load(self) -> None:
        """
        Load the storage data from a storage_storage_file.
        """
        try:
            with open(
                self._storage_path, "r", encoding="utf-8"
            ) as storage_storage_file:
                self._storage = json.load(storage_storage_file)
                logger.debug(f"Storage loaded from {self._storage_path}.")
        except FileNotFoundError:
            logger.warning(
                f"Storage storage_storage_file {self._storage_path} not found. Starting with an empty storage."
            )

    def save(self) -> None:
        """
        Save the storage data to a storage_storage_file.
        """
        try:
            with open(
                self._storage_path, "w", encoding="utf-8"
            ) as storage_storage_file:
                json.dump(
                    self._storage, storage_storage_file, ensure_ascii=False, indent=4
                )
                logger.debug(f"Storage saved to {self._storage_path}.")
        except IOError as error:
            logger.error(f"Failed to save storage to {self._storage_path}: {error}")

    def set(self, key: str, key_value: dict) -> None:
        """
        Set a key-value pair in the storage.
        """
        self._storage[key] = key_value
        logger.debug(f"Set key {key} in storage.")

    def get(self, key: str) -> dict | None:
        """
        Retrieve the value for a given key.
        """
        return self._storage.get(key)

    def delete(self, key: str) -> None:
        """
        Delete a key-value pair from the storage.
        """
        if key in self._storage:
            self._storage.pop(key)
            logger.debug(f"Deleted key {key} from storage.")
        else:
            logger.warning(f"Attempted to delete non-existent key {key}.")
