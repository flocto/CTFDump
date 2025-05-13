import os
from collections import Counter
from Crypto.Cipher import AES

ESSAY_DIR = 'essays/'
essays = os.listdir(ESSAY_DIR)
# bad_essays = zipfile.ZipFile('bad_essays.zip', 'w')

disobeyed = 0
bits = []
props = []
for essay_idx in essays:
    essay = open(f'{ESSAY_DIR}{essay_idx}').read()
    sentences = essay.lower().split('.')
    words = essay.lower().split()
    paragraphs = essay.lower().split('\n\n')
    
    first_word = [sentence.split()[0] for sentence in sentences if sentence.strip()]
    # print(first_word)
    c = Counter(first_word)
    # print(essay_idx, c)

    # the_in_proportion = (c['the'] + c['in']) / len(first_word)
    prop = len(c) / len(first_word)
    props.append(prop)
    # print(len(sentences), len(c), f'{prop:.2%}')

    bad = False
    if len(sentences) > 45:
        bad = True
    elif prop < 0.55:
        bad = True
        # disobeyed += 1
    elif len(words) > 650:
        bad = True
        # disobeyed += 1
    else:
        # print(essay_idx, c)
        print(essay_idx, len(words), len(sentences), len(paragraphs), len(c), f'{prop:.2%}')

    if bad:
        disobeyed += 1
        bits.append('0')
    else:
        bits.append('1')

print(disobeyed)

print(''.join(bits))

nonce = bytes.fromhex('3d6b85f9299442b2219a44aee1345e16')
ct = bytes.fromhex('c88f0e97fbe289c7800a68c2aae64a1825e0405cca87f6360e5f194e43978e1772f09a5bd2812cf9db8cf9008be7e34222ed9ee22bf6188358a49ada4e6d5ae16e71b0807d414f')
tag = bytes.fromhex('c58e546b2fed995d0a6a723c8f10f6d1')

for i in range(128):
    if bits[i] == '1':
        test_key = bits.copy()
        test_key[i] = '0'
        test_key = int(''.join(test_key), 2)
        assert test_key.bit_count() == 64
        test_key = test_key.to_bytes(16, byteorder='big')
        cipher = AES.new(test_key, AES.MODE_GCM, nonce=nonce)
        try:
            cipher.decrypt_and_verify(ct, tag)
            print(f"Key: {test_key.hex()}")
            break
        except:
            pass

# import matplotlib.pyplot as plt

# plt.hist(props, bins=100)
# plt.xlabel('Proportion of unique words')
# plt.ylabel('Number of essays')
# plt.title('Essay Analysis')
# plt.show()