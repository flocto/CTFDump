import struct

def rev(data):
    data = [struct.unpack('<I', data[i:i+4])[0] for i in range(0, len(data), 4)]
    cat = 1667331072 # b'cat\x00'

    def dfs(n, depth = 0):
        block = data[29 * n:29 * (n + 1)]
        if depth == 4:
            if cat in block:
                return [block.index(cat)]
            return -1
        
        for i in range(29):
            dfs_result = dfs(block[i], depth + 1)
            if dfs_result != -1:
                return [i] + dfs_result
        return -1

    return dfs(0)

alpha = 'abcdefghijklmnopqrstuvwxyz_{}'

flag = ''
for i in range(1, 8):
    data = open(f'data{i}', 'rb').read()
    block = rev(data)
    block = [alpha[c] for c in block]
    print(''.join(block))
    flag += ''.join(block)

print(flag)


