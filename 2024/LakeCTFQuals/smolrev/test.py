import gdb

def parse_dump(dump):
    dat = b''
    for line in dump.splitlines():
        for part in line.split()[1:]:
            dat += int(part, 16).to_bytes(8, 'little')
    
    return dat

dump = gdb.execute('x/20gx $rax', to_string=True)
dat = parse_dump(dump)[:81]
board = [list(dat[i:i+9]) for i in range(0, len(dat), 9)]
board = [
    [x if x != 255 else 0 for x in row]
    for row in board
]
print(board)