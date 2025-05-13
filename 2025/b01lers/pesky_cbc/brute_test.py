import secrets
from Crypto.Cipher import AES
import itertools

def strxor(a, b, c):
    return bytes([x ^ y ^ z for x, y, z in zip(a, b, c)])

try:
    with open('./flag.txt', 'r') as f:
        flag = f.read()
except:
    flag = 'bctf{REDACTED}'

key1 = secrets.token_bytes(32)
key2 = secrets.token_bytes(32)

def pesky_decrypt(ciphertext):
    assert len(ciphertext) % 16 == 0

    iv1 = secrets.token_bytes(16)
    iv2 = secrets.token_bytes(16)

    c1 = AES.new(key1, AES.MODE_CBC, iv1)
    c2 = AES.new(key2, AES.MODE_CBC, iv2)

    return c1.decrypt(c2.decrypt(ciphertext))

def main():
    global c 
    cipher = AES.new(key2, AES.MODE_ECB)

    secret = secrets.token_bytes(16)
    enc_secret = cipher.encrypt(secret)

    # print('Here is the encrypted secret:')
    # print(enc_secret.hex())
    # print()

    # print('Here are some hints for you ^_^')
    pts = []
    cts = []
    for _ in range(8):
        random_value = secrets.token_bytes(16)
        ciphertext = cipher.encrypt(random_value)
        # print(random_value.hex())
        # print(ciphertext.hex())
        pts.append(random_value)
        cts.append(ciphertext)
    # print()

    for i, j in itertools.product(range(8), repeat=2):
        if i == j:
            continue
        pt0, pt1 = pts[i], pts[j]
        ct0 = cts[i]
        if strxor(pt0, pt1, ct0) == enc_secret:
            print(f"Found secret: {enc_secret.hex()}")
            c += 1
    # while True:
    #     print('Options:')
    #     print('1: pesky decrypt')
    #     print('2: guess secret')
    #     choice = input('>> ').strip()

    #     if choice == '1':
    #         ciphertext = bytes.fromhex(input('>> '))
    #         print(pesky_decrypt(ciphertext).hex())
    #     elif choice == '2':
    #         guess = bytes.fromhex(input('>> '))
    #         if secret == guess:
    #             print('Here is your flag :)')
    #             print(flag)
    #             return
    #         else:
    #             print('lmao skill issue')
    #             return
    #     else:
    #         print('Invalid Choice')
    #         return

if __name__ == '__main__':
    c = 0
    for i in range(10000):
        main()
    

