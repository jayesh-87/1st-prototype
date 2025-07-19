import requests
from web3 import Web3
import json

# 1. Call the Flask API
response = requests.get("http://127.0.0.1:5000/recommendation")
recommendation = response.json()["recommendation"]
print(f"Model recommends: {recommendation}")

# 2. Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
assert web3.is_connected(), "Failed to connect to Ganache"

# 3. Load contract
with open("StockAdvisorABI.json") as f:
    abi = json.load(f)

contract_address = Web3.to_checksum_address("0xedb1d96ca1397c98502bc1b74870a9998f65918c")
contract = web3.eth.contract(address=contract_address, abi=abi)

# 4. Send transaction
account = web3.eth.accounts[0]
tx_hash = contract.functions.updateRecommendation(recommendation).transact({"from": account})
web3.eth.wait_for_transaction_receipt(tx_hash)
print("Smart contract updated successfully!")
