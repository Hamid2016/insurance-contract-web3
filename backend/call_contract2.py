from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv
import os
import json
# this code is call_contract.py plus ability to use .env
# this script will read setting from .env

# Load environment variables from .env file
load_dotenv()

# Connect to Ethereum network
alchemy_url = os.getenv("ALCHEMY_URL")
web3 = Web3(Web3.HTTPProvider(alchemy_url))

# Check connection
if not web3.is_connected():
    print("Failed to connect to the Ethereum network")
    exit()

# Contract details
contract_address = os.getenv("CONTRACT_ADDRESS")
contract_abi = json.loads(os.getenv("CONTRACT_ABI"))

# Instantiate the contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Account details
account_address = os.getenv("ACCOUNT_ADDRESS")
private_key = os.getenv("PRIVATE_KEY")

# Function 1: Create a new policy
def create_policy(policy_name, premium, coverage_amount):
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
        print(f"Transaction successful: {receipt.transactionHash.hex()}")
    except Exception as e:
        print(f"Error: {e}")

# Function 2: Get all policies
def get_policies():
    try:
        # Call the getPolicies function
        policies = contract.functions.getPolicies().call({"from": account_address})
        for policy in policies:
            print(f"Policy Name: {policy[0]}, Premium: {policy[1]}, Coverage: {policy[2]}, Active: {policy[3]}")
    except Exception as e:
        print(f"Error: {e}")

# Example Usage
create_policy("Car3 Insurance", 300, 30000)  # Replace with actual values
get_policies()
