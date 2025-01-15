class InMemoryStorage:
    """
    In-memory storage implementation
    """
    def __init__(self):
        """
        Initialize an empty data dictionary
        """
        self.data = {}

    def set(self, key:str, value:dict):
        """
        Set a key-value pair in the storage
        """
        self.data[key] = value

    def get(self, key:str):
        """
        Retrieve the value for a given key
        """
        return self.data.get(key, None)

    def update(self, key:str, value:dict):
        """
        Update the value for a given key
        """
        if key in self.data:
            self.data[key] = value
        else:
            print(f"Key {key} not found.")

    def delete(self, key:str):
        """
        Delete a key-value pair from the storage
        """
        if key in self.data:
            del self.data[key]
        else:
            print(f"Key {key} not found.")
