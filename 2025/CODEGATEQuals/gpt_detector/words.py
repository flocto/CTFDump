import os
from collections import Counter
from Crypto.Cipher import AES
import zipfile

essays = os.listdir('essays/')
bad_essays = zipfile.ZipFile('bad_essays.zip', 'w')

disobeyed = 0
bits = []
for essay_idx in essays:
    essay = open(f'essays/{essay_idx}').read()
    essay = essay.replace('.', ' ')
    essay = essay.replace(',', ' ')
    essay = essay.replace('!', ' ')
    essay = essay.replace('?', ' ')
    essay = essay.replace('(', ' ')
    essay = essay.lower().split()
    # print(len(essay))
    if len(essay) > 600:
        print(essay_idx)
        print(len(essay))
        bits.append('0')
        disobeyed += 1
        bad_essays.write(f'essays/{essay_idx}', f'bad_essays/{essay_idx}')
    else:
        bits.append('1')
        # print(len(essay))
        # essay = Counter(essay)
        # print(essay.most_common(25))

print(''.join(bits))

# print(disobeyed)
# print(bits)

# nonce = bytes.fromhex('3d6b85f9299442b2219a44aee1345e16')
# ct = bytes.fromhex('c88f0e97fbe289c7800a68c2aae64a1825e0405cca87f6360e5f194e43978e1772f09a5bd2812cf9db8cf9008be7e34222ed9ee22bf6188358a49ada4e6d5ae16e71b0807d414f')
# tag = bytes.fromhex('c58e546b2fed995d0a6a723c8f10f6d1')

# for i in range(128):
#     if bits[i] == '1':
#         test_key = bits.copy()
#         test_key[i] = '0'
#         test_key = int(''.join(test_key), 2)
#         assert test_key.bit_count() == 64
#         test_key = test_key.to_bytes(16, byteorder='big')
#         cipher = AES.new(test_key, AES.MODE_GCM, nonce=nonce)
#         try:
#             cipher.decrypt_and_verify(ct, tag)
#             print(f"Key: {test_key.hex()}")
#             break
#         except:
#             pass

#         inv_key = bits.copy()
#         inv_key[i] = '0'
#         inv_key = [int(b) ^ 1 for b in inv_key]
#         inv_key = int(''.join(map(str, inv_key)), 2)
#         assert inv_key.bit_count() == 64
#         inv_key = inv_key.to_bytes(16, byteorder='big')
#         cipher = AES.new(inv_key, AES.MODE_GCM, nonce=nonce)
#         try:
#             cipher.decrypt_and_verify(ct, tag)
#             print(f"Key: {inv_key.hex()}")
#             break
#         except:
#             pass
