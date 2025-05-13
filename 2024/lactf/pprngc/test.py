import random
from pwn import process
# nc chall.lac.tf 31173

def spam():
    # r = remote('chall.lac.tf', 31173, level='error')
    r = process(['python3', 'local.py'])

    seed_out = r.recvline_contains(b':').decode().split()[-1]
    print(seed_out)
    seed = None

    for i in range(5):
        r.sendlineafter(b'guess seed ', b'2')
        rnum = random.randint(0, 2**8-1)
        r.sendlineafter(b'! ', str(rnum).encode())
        res = r.recvline().strip().decode()
        # print(rnum, res)

        if seed_out == res:
            seed = rnum
            break
    
    if seed is None:
        r.sendlineafter(b'guess seed ', b'4')
        r.sendlineafter(b'! ', str(seed).encode())
        print(r.recvline())
        r.close()
        return False
    else:
        r.sendlineafter(b'guess seed ', b'4')
        r.sendlineafter(b'! ', str(seed).encode())
        print(r.recvline())
        r.close()
        return True
    
i = 0
while True:
    print(i)
    i += 1
    if spam():
        break

