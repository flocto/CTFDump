import secrets
from Crypto.Cipher import AES

key1 = secrets.token_bytes(32)
key2 = secrets.token_bytes(32)

cipher = AES.new(key2, AES.MODE_ECB)
test_cipher = AES.new(key1, AES.MODE_ECB)

def get_blocks(ciphertext):
    return [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]

pt = []
ct = []
for _ in range(2):
    random_value = secrets.token_bytes(16)
    ciphertext = cipher.encrypt(random_value)
    print(random_value.hex())
    print(ciphertext.hex())
    pt.append(random_value)
    ct.append(ciphertext)

def pesky_decrypt(ciphertext):
    assert len(ciphertext) % 16 == 0

    iv1 = secrets.token_bytes(16)
    iv2 = secrets.token_bytes(16)

    c1 = AES.new(key1, AES.MODE_CBC, iv1)
    c2 = AES.new(key2, AES.MODE_CBC, iv2)

    inner = c2.decrypt(ciphertext)
    # print_blocks(inner)
    return c1.decrypt(inner)

def random_decrypt(ciphertext, key):
    assert len(ciphertext) % 16 == 0

    iv = secrets.token_bytes(16)

    c = AES.new(key, AES.MODE_CBC, iv)

    return c.decrypt(ciphertext)

def print_blocks(ciphertext):
    print(" ".join(f"{block.hex()}" for block in get_blocks(ciphertext)))


def strxor(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

def dec(data):
    return test_cipher.decrypt(data)

def dec2(data):
    return cipher.decrypt(data)

secret = b'@' * 16
enc_secret = cipher.encrypt(secret)

ZERO = b'\x00' * 16

testA = b'A' * 16
testB = b'B' * 16

# data = ZERO * 2 + testA
# ciphertext = pesky_decrypt(data)
# print_blocks(ciphertext)
# last = ciphertext[-16:]
# assert last == strxor(dec2(ZERO), dec(dec2(testA)))

# data = last + ZERO + testB
# ciphertext = pesky_decrypt(data)
# print_blocks(ciphertext)
# last = ciphertext[-16:]
# assert last == strxor(dec(dec2(testA)), dec(dec2(testB)))

# data = last + ct[0] + testB
# ciphertext = pesky_decrypt(data)
# print_blocks(ciphertext)
# last = ciphertext[-16:]
# assert last == strxor(dec(dec2(testA)), pt[0])