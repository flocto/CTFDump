code = open('download.html').readlines()
code = [line.strip() for line in code[311:423]]

# code = open('index.html').readlines()
# code = [line.strip() for line in code[34:145]]

import json

attrs = json.loads(open('attrs.json').read())   

# print(attrs)

ops = [
    'add',
    'sub',
    'mul',
    'mod',
    'xor',
    'pop',
    'load',
    'cmp',
    'and',
    'shift'
]

dump = []
for line in code:
    parts = line.split('.')[1:] # first one doesnt matter
    for part in parts:
        if part in attrs:
            dump.append(ops[attrs[part]])
        else:
            dump.append(f'push {len(part) % 16}')
    # dump.append('=====')
    
with open('dump.txt', 'w') as f:
    for line in dump:
        f.write(line + '\n')