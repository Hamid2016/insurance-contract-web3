from web3 import Web3
from eth_account import Account

# Connect to Ethereum network (Alchemy or Infura URL)
alchemy_url = "https://eth-sepolia.g.alchemy.com/v2/JP4o2D0nluglljXXm47COL24z3Z2rOJ4"
web3 = Web3(Web3.HTTPProvider(alchemy_url))

# Check connection
if not web3.is_connected():
    print("Failed to connect to the Ethereum network")
    exit()

# Contract details
contract_address = "0x71aD7432B246E863b1aFED1f147937820dD327e9"  # Replace with your deployed contract address
abi = [  # Replace this with your contract's ABI
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "insured", "type": "address"},
            {"indexed": False, "internalType": "string", "name": "policyName", "type": "string"},
            {"indexed": False, "internalType": "uint256", "name": "premium", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "coverageAmount", "type": "uint256"}
        ],
        "name": "PolicyCreated",
        "type": "event"
    },
    {
        "inputs": [
            {"internalType": "string", "name": "_policyName", "type": "string"},
            {"internalType": "uint256", "name": "_premium", "type": "uint256"},
            {"internalType": "uint256", "name": "_coverageAmount", "type": "uint256"}
        ],
        "name": "createPolicy",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getPolicies",
        "outputs": [
            {
                "components": [
                    {"internalType": "string", "name": "policyName", "type": "string"},
                    {"internalType": "uint256", "name": "premium", "type": "uint256"},
                    {"internalType": "uint256", "name": "coverageAmount", "type": "uint256"},
                    {"internalType": "bool", "name": "isActive", "type": "bool"}
                ],
                "internalType": "struct Insurance.Policy[]",
                "name": "",
                "type": "tuple[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

# Instantiate the contract
contract = web3.eth.contract(address=contract_address, abi=abi)

# Set your account (replace with your private key and wallet address)
account = "0x2D69cad8789CCC676dAFf43C5e63E7523991F8A5"  # Replace with your wallet address
private_key = "013b3cfaba77202b8c99c0f722ee0a01249b5b70a952b0a2cc7a3d87a87eec2f"  # Replace with your private key

# Function 1: Create a new policy
def create_policy(policy_name, premium, coverage_amount):
    try:
        # Build the transaction
        transaction = contract.functions.createPolicy(
            policy_name,
            premium,
            coverage_amount
        ).build_transaction({
            "from": account,
            "gas": 210000,
            "gasPrice": web3.to_wei("5", "gwei"),
            "nonce": web3.eth.get_transaction_count(account),
        })

        # Sign the transaction using the updated method
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
        policies = contract.functions.getPolicies().call({"from": account})
        for policy in policies:
            print(f"Policy Name: {policy[0]}, Premium: {policy[1]}, Coverage: {policy[2]}, Active: {policy[3]}")
    except Exception as e:
        print(f"Error: {e}")

# Example Usage
create_policy("Personal Insurance", 200, 30000)  # Replace with actual values
get_policies()
