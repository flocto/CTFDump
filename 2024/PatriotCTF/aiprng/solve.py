from pwn import process
import string

def test_c(c):
    inp = c * 0x20
    p = process('./ai_rnd', level='error')
    p.sendline(inp.encode())
    res = p.recvall()
    p.close()
    return res.decode().strip().split()

# for i in range(10):
#     print(test_c('p'))

# exit()



target = 'a5 39 24 90 a8 a5 88 77 26 e4 3c 14 03 1e ba 3c 7d bb dc d6 aa 90 50 c9 0f aa dd 57 33 e1 a4 c7'.split()
print(len(target))

flag = ["?" for _ in range(0x20)]
# alpha = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_{}"
alpha = string.printable

for c in alpha:
    out = test_c(c)

    for i in range(0x20):
        if out[i] == target[i]:
            flag[i] = c
            print("".join(flag))