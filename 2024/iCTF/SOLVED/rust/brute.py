from pwn import process

key = int('0x883085554737383682184979', 16)

def test_key(test):
    p = process('./rust', level='error')
    p.sendlineafter(b'Enter the message:', b'i')
    p.sendlineafter(b'hex): ', test.encode())
    ret = p.recvline_contains(b'Encrypted: ')
    ret = eval(ret.split(b' ')[1].decode())
    return ret

def test_msg(msg):
    p = process('./rust', level='error')
    p.sendlineafter(b'Enter the message:', msg)
    p.sendlineafter(b'hex): ', b'883085554737383682184979')
    ret = p.recvline_contains(b'Encrypted: ')
    ret = eval(ret.split(b' ')[1].decode())
    return ret

enc = [-42148619422891531582255418903, -42148619422891531582255418927, -42148619422891531582255418851, -42148619422891531582255418907, -42148619422891531582255418831, -42148619422891531582255418859, -42148619422891531582255418855, -42148619422891531582255419111, -42148619422891531582255419103, -42148619422891531582255418687, -42148619422891531582255418859, -42148619422891531582255419119, -42148619422891531582255418843, -42148619422891531582255418687, -42148619422891531582255419103, -42148619422891531582255418907, -42148619422891531582255419107, -42148619422891531582255418915, -42148619422891531582255419119, -42148619422891531582255418935, -42148619422891531582255418823]

alpha = b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_{}'

dec = [0 for _ in range(len(enc))]

for c in alpha:
    msg = bytes([c])
    enc_test = test_msg(msg)[0]
    for i, e in enumerate(enc):
        if e == enc_test:
            dec[i] = c

    print(bytes(dec))