from pwn import process
from tqdm import trange

target = open('flag_enc', 'rb')
target = bytes.fromhex(target.read().decode().strip())
print(target)

def test_inp(inp):
    p = process("./chas_elf", level='error')
    p.sendline(inp)
    enc = p.recvline()
    enc = bytes.fromhex(enc.decode().strip())
    p.close()
    return enc

start = 67
end = 33

flag = [None] * 65
flag[0] = start
flag[64] = end
for i in range(128):
    inp = bytes([start]) + bytes([i]) * 63 + bytes([end])
    try:
        enc = test_inp(inp)
        for j in range(64):
            if enc[j] == target[j]:
                flag[j] = i
                # if flag[j] is None:
                #     flag[j] = i
                # else:
                #     if flag[j] != i:
                #         print(f'Conflict: {i} != {flag[j]}')
    except Exception as e:
        # print(i, e)
        pass

print(flag)
print(bytes(flag))

# inp = b'A' * 64 + b'}'
# enc = test_inp(inp)
# inp = b'B' * 64 + b'}' 
# enc = test_inp(inp)
# inp = b'A' * 32 + b'B' * 32 + b'}'
# enc = test_inp(inp)

# candidates = []
# for last in trange(33, 128):
#     for i in range(33, 128):
#         inp = bytes([i]) * 64 + bytes([last])
#         try:
#             # print(inp)
#             enc = test_inp(inp)
#             if enc[0] == target[0]:
#                 print(f'Found: {chr(i)}, {chr(last)}')
#                 candidates.append((i, last))
#                 break
#         except Exception as e:
#             # print(i, last, e)
#             pass

# print(candidates)

# flag = [None] * 64
# for i in range(128):
#     inp = b'A' + bytes([i]) * 63 + b'}'
#     try:
#         enc = test_inp(inp)
#         # if enc[0] == target[0]:
#         #     print(f'Found: {chr(i)}')
#         #     break
#         for j in range(64):
#             if enc[j] == target[j]:
#                 if flag[j] is None:
#                     flag[j] = i
#                 else:
#                     if flag[j] != i:
#                         print(f'Conflict: {i} != {flag[j]}')
#     except Exception as e:
#         print(i, e)

# print(flag)

# candidates = [(67, 33), (97, 35), (47, 36), (116, 39), (53, 41), (119, 45), (123, 48), (35, 49), (108, 50), (111, 51), (67, 56), (69, 60), (47, 65), (86, 66), (110, 68), (79, 69), (48, 70), (123, 71), (54, 72), (76, 73), (38, 74), (90, 76), (39, 79), (48, 80), (53, 81), (45, 86), (47, 89), (67, 90), (65, 92), (90, 94), (57, 95), (48, 96), (127, 102), (123, 104), (83, 106), (33, 107), (125, 108), (73, 113), (83, 118), (39, 119), (111, 120), (63, 123), (105, 125), (83, 127)]
# for start, end in candidates:
#     flag = [None] * 64
#     flag[0] = start
#     for i in range(128):
#         inp = bytes([start]) + bytes([i]) * 63 + bytes([end])
#         try:
#             enc = test_inp(inp)
#             for j in range(64):
#                 if enc[j] == target[j]:
#                     if flag[j] is None:
#                         flag[j] = i
#                     # else:
#                     #     if flag[j] != i:
#                     #         print(f'Conflict: {i} != {flag[j]}')
#         except Exception as e:
#             # print(i, e)
#             pass

#     try:
#         print(flag)
#         print(bytes(flag))
#     except Exception as e:
#         pass