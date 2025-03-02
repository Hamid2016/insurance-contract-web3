from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Initialize Jinja2Templates with the directory where your HTML files are stored
templates = Jinja2Templates(directory="../templates")

# Connect to Ethereum network
alchemy_url = os.getenv("ALCHEMY_URL")
web3 = Web3(Web3.HTTPProvider(alchemy_url))

# Ensure successful connection
if not web3.is_connected():
    raise HTTPException(status_code=500, detail="Failed to connect to the Ethereum network")

# Contract details from .env
contract_address = os.getenv("CONTRACT_ADDRESS")
contract_abi = json.loads(os.getenv("CONTRACT_ABI"))

# Instantiate the contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Account details from .env
account_address = os.getenv("ACCOUNT_ADDRESS")
private_key = os.getenv("PRIVATE_KEY")

# Route to render index.html
@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Function to create a new policy
@app.get("/create-policy")
async def create_policy(policy_name: str, premium: int, coverage_amount: int):
    try:
        # Get the latest gas price
        gas_price = web3.eth.gas_price

        # Build the transaction
        transaction = contract.functions.createPolicy(
            policy_name,
            premium,
            coverage_amount
        ).build_transaction({
            "from": account_address,
            "gas": 210000,
            "gasPrice": gas_price + web3.to_wei(2, "gwei"),  # Increase gas price slightly
            "nonce": web3.eth.get_transaction_count(account_address),
        })

        # Sign the transaction
        signed_tx = Account.sign_transaction(transaction, private_key)

        # Send the transaction
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

        # Wait for confirmation
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        return {"message": f"Transaction successful: {receipt.transactionHash.hex()}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Function to get all policies
@app.get("/get-policies")
async def get_policies():
    try:
        # Call the getPolicies function
        policies = contract.functions.getPolicies().call({"from": account_address})

        # Return the policies as a list of dictionaries
        return [
            {
                "policyName": policy[0],
                "premium": policy[1],
                "coverageAmount": policy[2],
                "isActive": policy[3],
            }
            for policy in policies
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Run the application (if executed directly)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)  # Adjust host and port as needed
