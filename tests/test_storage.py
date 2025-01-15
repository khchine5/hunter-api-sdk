import pytest
from hunter_sdk.storage import InMemoryStorage

def test_storage_create_and_read():
    storage = InMemoryStorage()
    storage.set("test_key", {"value": "test_value"})
    assert storage.get("test_key") == {"value": "test_value"}

def test_storage_update():
    storage = InMemoryStorage()
    storage.set("test_key", {"value": "old_value"})
    storage.set("test_key", {"value": "new_value"})
    assert storage.get("test_key") == {"value": "new_value"}

def test_storage_delete():
    storage = InMemoryStorage()
    storage.set("test_key", {"value": "test_value"})
    storage.delete("test_key")
    assert storage.get("test_key") is None
