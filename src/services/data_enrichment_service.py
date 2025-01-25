import requests
import logging
from fastapi import HTTPException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataEnrichmentService:
    def __init__(self):
        # Define external API endpoints
        self.external_api_endpoints = {
            "user_info": "https://api.example.com/userinfo",
            "transaction_details": "https://api.example.com/transaction",
            # Add more endpoints as needed
        }

    def enrich_user_data(self, user_id: str):
        """Enrich user data by fetching additional information from external APIs."""
        try:
            response = requests.get(f"{self.external_api_endpoints['user_info']}?id={user_id}")
            response.raise_for_status()  # Raise an error for bad responses
            user_data = response.json()
            logger.info(f"Successfully enriched data for user ID: {user_id}")
            return user_data
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred while fetching user data: {http_err}")
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch user data")
        except Exception as err:
            logger.error(f"An error occurred while enriching user data: {err}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def enrich_transaction_data(self, transaction_id: str):
        """Enrich transaction data by fetching additional information from external APIs."""
        try:
            response = requests.get(f"{self.external_api_endpoints['transaction_details']}?id={transaction_id}")
            response.raise_for_status()  # Raise an error for bad responses
            transaction_data = response.json()
            logger.info(f"Successfully enriched data for transaction ID: {transaction_id}")
            return transaction_data
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred while fetching transaction data: {http_err}")
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch transaction data")
        except Exception as err:
            logger.error(f"An error occurred while enriching transaction data: {err}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

# Example usage
if __name__ == "__main__":
    service = DataEnrichmentService()
    user_info = service.enrich_user_data("12345")
    print(user_info)

    transaction_info = service.enrich_transaction_data("67890")
    print(transaction_info)
