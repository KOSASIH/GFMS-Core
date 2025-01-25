import os
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from web3 import Web3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="GFMS-Core Smart Contract Management API", version="1.0.0")

# Connect to Ethereum network (replace with your own provider)
infura_url = os.getenv("INFURA_URL", "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID")
web3 = Web3(Web3.HTTPProvider(infura_url))

# Check if connected to the Ethereum network
if not web3.isConnected():
    logger.error("Failed to connect to the Ethereum network.")
    raise Exception("Ethereum network connection error.")

# Data model for smart contract interaction
class SmartContract(BaseModel):
    address: str
    abi: dict

# In-memory storage for smart contracts (replace with a database in production)
smart_contracts = {}

# Endpoint to deploy a new smart contract
@app.post("/smart_contract/deploy", response_model=dict, tags=["Smart Contracts"])
async def deploy_smart_contract(contract: SmartContract):
    """Deploy a new smart contract."""
    try:
        # Create contract instance
        contract_instance = web3.eth.contract(address=contract.address, abi=contract.abi)
        # Here you would typically send a transaction to deploy the contract
        # For demonstration, we will just log the contract address and ABI
        smart_contracts[contract.address] = contract.abi
        logger.info(f"Smart contract deployed at address: {contract.address}")
        return {"message": "Smart contract deployed successfully", "address": contract.address}
    except Exception as e:
        logger.error(f"Error deploying smart contract: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to deploy smart contract")

# Endpoint to interact with a smart contract
@app.post("/smart_contract/interact", response_model=dict, tags=["Smart Contracts"])
async def interact_smart_contract(address: str, method: str, *args):
    """Interact with a smart contract method."""
    if address not in smart_contracts:
        raise HTTPException(status_code=404, detail="Smart contract not found")
    
    try:
        contract_instance = web3.eth.contract(address=address, abi=smart_contracts[address])
        # Call the specified method on the smart contract
        result = getattr(contract_instance.functions, method)(*args).call()
        logger.info(f"Interacted with smart contract at {address}, method: {method}, result: {result}")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error interacting with smart contract: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to interact with smart contract")

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", 8000)))
