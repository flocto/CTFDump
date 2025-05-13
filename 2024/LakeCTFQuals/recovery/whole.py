import json
from web3 import Web3
from pwn import *

from eth_account._utils.signing import extract_chain_id, to_standard_v
from eth_account._utils.legacy_transactions import serializable_unsigned_transaction_from_dict
import string
CHAIN_ID = 31337

# Token: b'cea459c05042ee656ab016fcee8a6640d930261c784d9dedee1fb86380202961'
# URL: https://challs.polygl0ts.ch:8545/cea459c05042ee656ab016fcee8a6640d930261c784d9dedee1fb86380202961
# RPC endpoint: https://challs.polygl0ts.ch:8545/cea459c05042ee656ab016fcee8a6640d930261c784d9dedee1fb86380202961
# Private key: 0x9fb7ce7919f23611e67a29069e439df007ef02f2d73f0604cdc34caff41c24af
# Challenge: 0x968473346540Fd46128FfBf89492d2C17C7E36a3


with open('abi.json', 'r') as openfile:
    abi = json.load(openfile)
rpc_url = "https://challs.polygl0ts.ch:8545/cea459c05042ee656ab016fcee8a6640d930261c784d9dedee1fb86380202961"
challenge_addr = "0x968473346540Fd46128FfBf89492d2C17C7E36a3"
priv_key = "0x9fb7ce7919f23611e67a29069e439df007ef02f2d73f0604cdc34caff41c24af"

w3 = Web3(Web3.HTTPProvider(rpc_url))
# Create smart contract instance
contract = w3.eth.contract(address=challenge_addr, abi=abi)

print(f"Is challenge solved: {contract.functions.isSolved().call()}")
blck = w3.eth.get_block(1)
tx_hash = blck.transactions[0] # contract deployment transaction
tx = w3.eth.get_transaction(tx_hash)
print(tx)

s = w3.eth.account._keys.Signature(vrs=(
    to_standard_v(extract_chain_id(tx["v"])[1]),
    w3.to_int(tx["r"]),
    w3.to_int(tx["s"])
))

keys_to_get = ["to",
    "nonce",
    "value",
    "gas",
    "chainId",
    "maxFeePerGas",
    "maxPriorityFeePerGas",
    "type"]

if "chainId" not in tx:
    tx["chainId"] = 1

tt = {k:tx[k] for k in keys_to_get}
tt["data"] = tx["input"]

ut = serializable_unsigned_transaction_from_dict(tt)

public_key = s.recover_public_key_from_msg_hash(ut.hash())

print(public_key, public_key.to_checksum_address())

pk_bytes = public_key.to_bytes()

left = pk_bytes[:32]
right = pk_bytes[32:]
from randomshit import *
Qx = big_endian_to_int(left)
Qy = big_endian_to_int(right)
Q = Point(Qx, Qy, curve=secp256k1)
print(Q)