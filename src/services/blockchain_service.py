# src/services/blockchain_service.py

import logging
from sqlalchemy.orm import Session
from src.models.transaction import Transaction
from src.utils.blockchain_client import BlockchainClient  # Assuming you have a blockchain client utility

logger = logging.getLogger(__name__)

class BlockchainService:
    def __init__(self, db: Session):
        self.db = db
        self.blockchain_client = BlockchainClient()

    def send_transaction(self, transaction: Transaction):
        try:
            # Call the blockchain API to send the transaction
            blockchain_response = self.blockchain_client.send_transaction(
                sender_id=transaction.sender_id,
                receiver_id=transaction.receiver_id,
                amount=transaction.amount
            )
            if blockchain_response['status'] == 'success':
                transaction.status = 'completed'
                logger.info(f"Blockchain transaction sent successfully for transaction {transaction.id}.")
            else:
                transaction.status = 'failed'
                logger.error(f"Blockchain transaction failed for transaction {transaction.id}: {blockchain_response['message']}")
        except Exception as e:
            transaction.status = 'failed'
            logger.error(f"Error sending blockchain transaction for transaction {transaction.id}: {str(e)}")
        finally:
            self.db.commit()
            self.db.refresh(transaction)

    def get_transaction_status(self, transaction_id: str):
        try:
            # Call the blockchain API to get the transaction status
            status_response = self.blockchain_client.get_transaction_status(transaction_id)
            logger.info(f"Transaction status for {transaction_id}: {status_response['status']}")
            return status_response
        except Exception as e:
            logger.error(f"Error retrieving blockchain transaction status for {transaction_id}: {str(e)}")
            return None
