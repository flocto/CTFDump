import gdb

cmds = '''
set $rcx = 0
c
set $rax = 0x217fd7a7
c
set $rcx = 0
c
set $rcx = 0
'''

for cmd in cmds.split('\n'):
    cmd = cmd.strip()
    if not cmd:
        continue
    print(f'Executing: {cmd}')
    gdb.execute(cmd)