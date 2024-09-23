from pwn import remote
from tqdm import tqdm
# nc chal.competitivecyber.club 6001

r = remote('chal.competitivecyber.club', 6001)

block_size = 16

def send_remote(data):
    r.sendlineafter(b'> ', data.encode())
    resp = r.recvline().strip().decode().split()[-1]
    resp = bytes.fromhex(resp)
    blocks = [resp[i:i+block_size] for i in range(0, len(resp), block_size)]
    return blocks

alpha = 'pctf{}_abcdefghijklmnopqrstuvwxyz0123456789'
known = ''

while len(known) < 13:
    rem = 16 % (len(known) + 1)
    prefill = '_' * rem

    for c in tqdm(alpha):
        chunk = known + c
        block = prefill + chunk * (16 // len(chunk))
        payload = block + block[:-len(chunk)]
        
        blocks = send_remote(payload)

        if blocks[0] == blocks[1]:
            known += c
            print(f'{payload, len(payload)} -> {blocks}')
            print(f'Found: {known}')
            break

    # break