import pytest
from web3 import Web3
from src.blockchain_service import BlockchainService  # Adjust the import based on your project structure

# Mocking the Web3 connection for testing
class MockWeb3:
    def __init__(self):
        self.eth = MockEth()

class MockEth:
    def sendTransaction(self, transaction):
        # Simulate sending a transaction and return a mock transaction hash
        return "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"

    def getTransaction(self, tx_hash):
        # Simulate getting a transaction receipt
        return {
            "hash": tx_hash,
            "status": 1,  # Simulate a successful transaction
        }

@pytest.fixture
def blockchain_service():
    # Create a mock instance of the BlockchainService
    mock_web3 = MockWeb3()
    return BlockchainService(web3=mock_web3)

def test_send_transaction(blockchain_service):
    # Test sending a transaction
    transaction = {
        "to": "0xRecipientAddress",
        "value": 1000000000000000000,  # 1 Ether in Wei
        "gas": 2000000,
        "gasPrice": 20000000000,  # 20 Gwei
        "nonce": 0,
    }
    tx_hash = blockchain_service.send_transaction(transaction)
    assert tx_hash == "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"

def test_get_transaction(blockchain_service):
    # Test getting a transaction
    tx_hash = "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    transaction = blockchain_service.get_transaction(tx_hash)
    assert transaction["hash"] == tx_hash
    assert transaction["status"] == 1  # Check if the transaction was successful

def test_get_transaction_failure(blockchain_service):
    # Test getting a transaction with a non-existent hash
    tx_hash = "0xNonExistentTransactionHash"
    with pytest.raises(Exception) as excinfo:
        blockchain_service.get_transaction(tx_hash)
    assert "Transaction not found" in str(excinfo.value)
