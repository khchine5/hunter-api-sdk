# **Hunter API SDK**

This SDK provides an interface for interacting with the [Hunter.io Email Verifier API](https://hunter.io/api-documentation/v2). It includes email validation functionality and utilizes an in-memory storage solution for caching results.

---

## **Features**

- Validate email addresses via the Hunter.io API.
- Cache results to minimize redundant API requests.
- Handle API rate-limiting and retries for `202 Accepted` responses.
- Easy-to-use and extensible architecture.

---

## **Requirements**

- Python 3.8+
- A Hunter.io API key

---

## **Installation**

Clone the repository and install the package using `pip`:

```bash
git clone https://github.com/khchine5/hunter-api-sdk.git
cd hunter-api-sdk
pip install .
```

Or install directly from GitHub:

```bash
pip install git+https://github.com/khchine5/hunter-api-sdk.git
```

---

## **Usage**

### **Basic Example**

```python
from hunter_sdk.hunter_service import HunterService
from hunter_sdk.storage import InMemoryStorage

# Initialize the SDK
api_key = "your_hunter_api_key"
storage = InMemoryStorage()
hunter_service = HunterService(api_key=api_key, storage=storage)

# Validate an email
email = "test@example.com"
result = hunter_service.validate_email(email)

# Output the result
if result:
    print(f"Validation Result: {result}")
else:
    print("Failed to validate email.")
```

---

## **Features**

### **Email Validation**

The `validate_email` method:
- Checks if the email result is already cached.
- Makes a request to the Hunter.io API if not cached.
- Handles retries for `202 Accepted` responses.
- Returns the validation result.

### **In-Memory Storage**

The SDK uses a simple in-memory dictionary to store results:
- `store(key, value)`: Stores a key-value pair.
- `retrieve(key)`: Retrieves the value for a key.
- `clear()`: Clears all stored data.

---

## **Testing**

The project includes unit tests using the `pytest` framework and the `responses` library for mocking HTTP requests.

### **Run Tests**

```bash
pytest tests/
```

---

## **Logging**

The SDK uses Python's `logging` module for debug and error messages. Enable debug-level logs to monitor API calls and retries:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

---

## **Configuration**

You can configure the following parameters in the `HunterService` class:

| Parameter       | Description                                   | Default |
|-----------------|-----------------------------------------------|---------|
| `api_key`       | Your Hunter.io API key                       | None    |
| `storage`       | Storage instance for caching results         | None    |
| `max_retries`   | Number of retries for `202 Accepted`         | 5       |
| `retry_delay`   | Delay (in seconds) between retries           | 5       |

---

## **API Rate-Limiting**

The API imposes daily rate limits per domain. The SDK handles retries for `202 Accepted` responses but does not automatically handle `429 Too Many Requests`. Make sure to monitor your usage.

---

## **License**

This project is licensed under the [MIT License](LICENSE).

---

## **Contributing**

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

1. Fork the repository.
2. Create a new branch for your feature.
3. Commit your changes.
4. Submit a pull request.

---

## **Contact**

For issues or questions, please open an issue in the GitHub repository or contact the maintainer.

