from pwn import remote
# nc chall.lac.tf 31172
r = remote('chall.lac.tf', 31172)

def get_flag():
    r.sendlineafter(b'> ', b'2')
    enc_flag = r.recvline().strip().split(b': ')[1]
    return enc_flag

def send_msg(msg):
    r.sendlineafter(b'> ', b'1')
    r.sendlineafter(b'?\n', msg.encode())
    ret = r.recvline()
    if b':' in ret:
        return ret.strip().split(b': ')[1]
    else:
        return ret.strip()
    
def get_perm(msg, perm):
    return [msg.index(c) for c in perm]

leaks = []
for i in range(600, 617):
    msg = 'A'*i
    enc_msg = send_msg(msg)
    if enc_msg == b'Are you trying to hack me?':
        leaks.append(i)
        print(f'Leaked: {i}')

print(leaks)