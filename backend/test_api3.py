from web3 import Web3

# Connect to Ethereum network via an RPC URL (e.g., Alchemy)
alchemy_url = "https://eth-sepolia.g.alchemy.com/v2/JP4o2D0nluglljXXm47COL24z3Z2rOJ4"
web3 = Web3(Web3.HTTPProvider(alchemy_url))

# Check connection
if web3.is_connected():
    print("Connected to Ethereum network")
else:
    print("Failed to connect")
    exit()

# Contract details
contract_address = "0x71aD7432B246E863b1aFED1f147937820dD327e9"
abi = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "insured", "type": "address"},
            {"indexed": False, "internalType": "string", "name": "policyName", "type": "string"},
            {"indexed": False, "internalType": "uint256", "name": "premium", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "coverageAmount", "type": "uint256"},
        ],
        "name": "PolicyCreated",
        "type": "event",
    },
    {
        "inputs": [
            {"internalType": "string", "name": "_policyName", "type": "string"},
            {"internalType": "uint256", "name": "_premium", "type": "uint256"},
            {"internalType": "uint256", "name": "_coverageAmount", "type": "uint256"},
        ],
        "name": "createPolicy",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
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
                    {"internalType": "bool", "name": "isActive", "type": "bool"},
                ],
                "internalType": "struct Insurance.Policy[]",
                "name": "",
                "type": "tuple[]",
            }
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "", "type": "address"},
            {"internalType": "uint256", "name": "", "type": "uint256"},
        ],
        "name": "policies",
        "outputs": [
            {"internalType": "string", "name": "policyName", "type": "string"},
            {"internalType": "uint256", "name": "premium", "type": "uint256"},
            {"internalType": "uint256", "name": "coverageAmount", "type": "uint256"},
            {"internalType": "bool", "name": "isActive", "type": "bool"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
]

# Instantiate contract
contract = web3.eth.contract(address=contract_address, abi=abi)

# Function to retrieve owner (replace 'owner' with the actual function/variable if applicable)
try:
    # Replace 'owner' with the correct method or variable to retrieve the owner's address
    owner_address = contract.functions.owner().call()
    print(f"Contract Owner Address: {owner_address}")
except Exception as e:
    print(f"Error retrieving owner: {e}")
