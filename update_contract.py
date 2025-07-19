import requests
from web3 import Web3
import json

# 1. Call the Flask API
response = requests.get("Your url with port/recommendation")
recommendation = response.json()["recommendation"]
print(f"Model recommends: {recommendation}")

# 2. Connect to Ganacheganache_url = os.getenv("GANACHE_URL")
ganache_url = os.getenv("GANACHE_URL")
web3 = Web3(Web3.HTTPProvider(ganache_url))
assert web3.is_connected(), "Failed to connect to Ganache"

# 3. Load contract
with open("StockAdvisorABI.json") as f:
    abi = json.load(f)

contract_address = Web3.to_checksum_address(os.getenv("CONTRACT_ADDRESS"))
contract = web3.eth.contract(address=contract_address, abi=abi)

# 4. Send transaction
account = web3.eth.accounts[account_index]
tx_hash = contract.functions.updateRecommendation(recommendation).transact({"from": account})
web3.eth.wait_for_transaction_receipt(tx_hash)
print("Smart contract updated successfully!")
