#!/usr/local/bin/python
from os import __dict__

value = 'valasdasd'
code = 'codedea'

assert all(32 <= ord(x) < 127 for x in code), 'cant read this'

def f():
    pass
    
f.__code__ = f.__code__.replace(co_names=(), co_code=bytes([
    124, 126,
    83
]))

print(f())