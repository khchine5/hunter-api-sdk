from hunter_sdk.storage import InMemoryStorage


def test_storage_create_and_read() -> None:
    storage = InMemoryStorage()
    storage.set("test_key", {"value": "test_value"})
    assert storage.get("test_key") == {"value": "test_value"}


def test_storage_update() -> None:
    storage = InMemoryStorage()
    storage.set("test_key", {"value": "old_value"})
    storage.set("test_key", {"value": "new_value"})
    assert storage.get("test_key") == {"value": "new_value"}


def test_storage_delete() -> None:
    storage = InMemoryStorage()
    storage.set("test_key", {"value": "test_value"})
    storage.delete("test_key")
    assert storage.get("test_key") is None


def test_storage_save() -> None:
    storage = InMemoryStorage()
    storage.set("test_key", {"value": "test_value"})
    storage.save()
    storage = InMemoryStorage()
    assert storage.get("test_key") == {"value": "test_value"}
    storage.delete("test_key")
    storage.save()
    storage = InMemoryStorage()
    assert storage.get("test_key") is None
