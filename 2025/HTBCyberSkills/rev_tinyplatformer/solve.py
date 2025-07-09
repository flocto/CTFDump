import itertools

for first in itertools.permutations(range(6), 6):
    for second in itertools.permutations(range(5), 5):
        for third in itertools.permutations(range(4), 4):
            secrets = [first, second, third]
            conds = [secrets[0][0] > secrets[0][2], 
                     secrets[0][1] < secrets[0][4], 
                     secrets[0][2] > secrets[0][5], 
                     secrets[0][3] > secrets[0][4], 
                     secrets[1][0] < secrets[1][4], 
                     secrets[1][2] < secrets[1][1], 
                     secrets[2][0] > secrets[2][1], 
                     secrets[2][2] > secrets[2][3]]
            if all(conds):
                key = (''.join(map(str, first)) + ''.join(map(str, second)) + ''.join(map(str, third))).encode()
                enc = b'}dvIA_\x00FV\x01A^\x01CoG\x03BD\x00]SO'

                dec = bytes(enc[i] ^ key[i % len(key)] for i in range(len(enc)))
                if dec.startswith(b'HTB{') and dec.endswith(b'}'):
                    print(dec.decode(), first, second, third)

                # flag = b'HTB{pl4tf0rm3r_r3vv1n_}'
                # key = bytes(flag[i] ^ enc[i] for i in range(len(flag)))
                # print(key.decode(), first, second, third)