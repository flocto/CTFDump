from pwn import *
context.arch = 'amd64'

test ='''
mov dword ptr [0x1408a0034], eax
'''

a = asm(test)
print(a)

test ='''
mov rbx, qword ptr [0x1408a0080]
'''

a = asm(test)
print(a)