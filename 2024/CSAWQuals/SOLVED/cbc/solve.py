from pwn import remote
from tqdm import trange
BLOCK_SIZE = 16
enc = open('out.txt', 'r').read().strip()
enc = bytes.fromhex(enc)

# nc cbc.ctf.csaw.io 9996
r = remote('cbc.ctf.csaw.io', 9996, level='error')

def test(q):
    global r
    try:
        r.sendlineafter(b'ciphertext: ', q.hex().encode())
        nxt = r.recvline()
        return nxt
    except Exception as e:
        r = remote('cbc.ctf.csaw.io', 9996, level='error')
        return test(q)
    
def is_padding_ok(msg):
    return b'Error' not in test(msg)

def attack_message(msg):

    cipherfake=[0] * 16
    plaintext = [0] * 16
    current = 0
    message=[]


    #I devide the list of bytes in blocks, and I put them in another list
    number_of_blocks = int(len(msg)/BLOCK_SIZE)
    blocks = [[]] * number_of_blocks
    for i in (range(number_of_blocks)):
        blocks[i] = msg[i * BLOCK_SIZE: (i + 1) * BLOCK_SIZE]

    for z in trange(16, len(blocks)-1):  #for each message, I calculate the number of block
        for itera in trange(1,17): #the length of each block is 16. I start by one because than I use its in a counter
            for v in range(256):
                cipherfake[-itera]=v
                if is_padding_ok(bytes(cipherfake)+blocks[z+1]): #the idea is that I put in 'is_padding_ok' the cipherfake(array of all 0) plus the last block
                                                                 #if the function return true I found the value
                    current=itera
                    plaintext[-itera]= v^itera^blocks[z][-itera]
                    break

            for w in range(1,current+1):
                cipherfake[-w] = plaintext[-w]^itera+1^blocks[z][-w] #for decode the second byte I must set the previous bytes with 'itera+1'

        print(f'Block {z+1}: {bytes(plaintext)}')
        message.extend(plaintext)
        # print(f'Message: {bytes(message)}')
        open('dump.txt', 'wb').write(bytes(message))

    return bytes(message)

pt = attack_message(enc)
open('dump.txt', 'wb').write(pt)