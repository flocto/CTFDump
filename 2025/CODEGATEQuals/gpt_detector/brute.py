import os
from collections import Counter
from Crypto.Cipher import AES

nonce = bytes.fromhex('3d6b85f9299442b2219a44aee1345e16')
ct = bytes.fromhex('c88f0e97fbe289c7800a68c2aae64a1825e0405cca87f6360e5f194e43978e1772f09a5bd2812cf9db8cf9008be7e34222ed9ee22bf6188358a49ada4e6d5ae16e71b0807d414f')
tag = bytes.fromhex('c58e546b2fed995d0a6a723c8f10f6d1')

idxs = [4, 5, 9, 10, 12, 13, 16, 17, 26, 30, 34, 35, 37, 38, 39, 42, 44, 45, 46, 47, 49, 50, 51, 52, 53, 54, 57, 58, 59, 61, 62, 63, 66, 68, 69, 70, 72, 74, 75, 76, 77, 78, 81, 82, 83, 86, 87, 88, 89, 90, 91, 96, 99, 103, 105, 107, 109, 111, 112, 117, 120, 121, 122, 126]
print(len(idxs))

bits = [1] * 128
for i in idxs:
    bits[i] = 0

# bits = bits[::-1]

key = int(''.join(map(str, bits)), 2).to_bytes(16, byteorder='big')
cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
print(cipher.decrypt(ct))