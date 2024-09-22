import subprocess

def f():
    pass

template = '''#!/usr/local/bin/python
from os import __dict__

value = 'valasdasd'
code = 'codedea'

assert all(32 <= ord(x) < 127 for x in code), 'cant read this'

def f():
    pass
    
f.__code__ = f.__code__.replace(co_names=(), co_code=bytes([
    124, <<I>>,
    83
]))

print(f())'''

from opcode import opmap

for i in range(32, 127):
    code = template.replace('<<I>>', str(i))
    open('tmp.py', 'w').write(code)

    with subprocess.Popen(['python', 'tmp.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        out, err = proc.communicate()
        if not err:
            print(i, out)
        else:
            print(i, err)


# import dis
# dis.dis(f)

# f()
