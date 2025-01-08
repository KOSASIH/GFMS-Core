# src/services/payment_gateway_service.py

import logging
from sqlalchemy.orm import Session
from src.models.transaction import Transaction
from src.utils.payment_gateway_client import PaymentGatewayClient  # Assuming you have a payment gateway client utility

logger = logging.getLogger(__name__)

class PaymentGatewayService:
    def __init__(self, db: Session):
        self.db = db
        self.payment_gateway_client = PaymentGatewayClient()

    def process_payment(self, transaction: Transaction):
        try:
            # Call the payment gateway API to process the payment
            response = self.payment_gateway_client.process_payment(
                sender_id=transaction.sender_id,
                receiver_id=transaction.receiver_id,
                amount=transaction.amount
            )
            if response['status'] == 'success':
                transaction.status = 'completed'
                logger.info(f"Payment processed successfully for transaction {transaction.id}.")
            else:
                transaction.status = 'failed'
                logger.error(f"Payment processing failed for transaction {transaction.id}: {response['message']}")
        except Exception as e:
            transaction.status = 'failed'
            logger.error(f"Error processing payment for transaction {transaction.id}: {str(e)}")
        finally:
            self.db.commit()
            self.db.refresh(transaction)

    def refund_payment(self, transaction: Transaction):
        try:
            # Call the payment gateway API to process the refund
            response = self.payment_gateway_client.refund_payment(transaction.id)
            if response['status'] == 'success':
                transaction.status = 'refunded'
                logger.info(f"Refund processed successfully for transaction {transaction.id}.")
            else:
                logger.error(f"Refund processing failed for transaction {transaction.id}: {response['message']}")
        except Exception as e:
            logger.error(f"Error processing refund for transaction {transaction.id}: {str(e)}")
        finally:
            self.db.commit()
            self.db.refresh(transaction)
