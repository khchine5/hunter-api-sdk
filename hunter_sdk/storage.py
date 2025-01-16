import json


class InMemoryStorage:
    """
    In-memory storage implementation
    """

    def __init__(self):
        """
        Initialize an empty data dictionary
        """
        self.data = {}
        self.storage_file = "data.json"
        self.load()

    def load(self, path: str = "data.json"):
        """
        Load the storage from a file
        """
        try:
            with open(path, "r") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            print(f"File {path} not found.")
            pass

    def set(self, key: str, value: dict):
        """
        Set a key-value pair in the storage
        """
        self.data[key] = value

    def get(self, key: str):
        """
        Retrieve the value for a given key
        """
        return self.data.get(key, None)

    def delete(self, key: str):
        """
        Delete a key-value pair from the storage
        """
        if key in self.data:
            del self.data[key]
        else:
            print(f"Key {key} not found.")

    def save(self, path: str = "data.json"):
        """
        Save the storage to a file
        """
        with open(path, "w") as f:
            json.dump(self.data, f)
