#!/usr/local/bin/python3
from time import sleep
import subprocess

inp = bytes.fromhex(input("> ")).decode()

for char in inp:
    if ord(char) > 256:
        print("hey, not cool !")
        exit()

# print(inp)

with subprocess.Popen(["python3", "Charcoal/charcoal.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
    print(proc.communicate(input=inp.encode())[0].decode())

print('bye')

