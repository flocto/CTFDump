import json
from web3 import Web3
from pwn import *

import string

# r = remote(args.get('HOST', "localhost"), args.get('PORT', 9256))
# chall.polygl0ts.ch 9056
r = remote("chall.polygl0ts.ch", 9056)

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