from key_gen import derive_key_from_password
from tqdm import tqdm
from Crypto.Cipher import AES

body = open('body.txt', 'rb').read()[976:976+32]
print(body)

keys = []
# for word in tqdm(open('wordlist.txt', 'r').read().split('\n')):
for word in ['HP Wolf Security', 'HP WOLF SECURITY', 'HP wolf security', 'hp wolf security', 'hp Wolf security', 'hp wolf Security', 'HP WOLF security', 'HP WOLF Security', 'hp WOLF SECURITY']:
    # if '123' not in word.lower(): 
    #     continue
    # print(word.strip())
    pwd = word.strip()
    key = derive_key_from_password(pwd).encode()
    keys.append(key)

    cipher = AES.new(bytes.fromhex(key.decode()), AES.MODE_ECB)
    # cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(body)

    # print(body[976:976+48], body[976+48:976+48+48])
    print(decrypted)

    if decrypted[:9] == decrypted[9:18]:
        print('Found key:', key)
        print('Decrypted:', decrypted)
        print('Password:', pwd)
        open('flag.bmp', 'wb').write(decrypted)
        # break

open('keys.txt', 'w').write(str(keys))