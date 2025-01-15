
from .hunter_service import HunterService
from .storage import InMemoryStorage

if __name__ == "__main__":
    # Initialize the in-memory storage and service
    storage = InMemoryStorage()
    api_key = "your_hunter_api_key_here"  # Replace with your actual Hunter.io API key
    hunter_service = HunterService(api_key, storage)

    # Verify an email address
    email_to_verify = "test@example.com"
    validation_result = hunter_service.verify_email(email_to_verify)
    
    if validation_result:
        print(f"Validation result for {email_to_verify}:")
        print(validation_result)

    # Retrieve stored validation result
    stored_result = hunter_service.get_validation_result(email_to_verify)
    if stored_result:
        print(f"Stored result for {email_to_verify}:")
        print(stored_result)
