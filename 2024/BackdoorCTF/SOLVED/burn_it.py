from pwn import remote
from collections import deque
# nc 34.45.235.239 8010
r = remote('34.45.235.239', 8010)

T = int(r.recvline_contains(b'objects : ').decode().strip().split()[-1])
for _ in range(T):
    n = int(r.recvline_contains(b'knots are : ').decode().strip().split()[-1])
    r.recvline_contains(b'"(knot_1) (knot_2)" :')

    edges = {}
    for _ in range(n - 1):
        a, b = map(int, r.recvline().decode().strip().split())
        if a not in edges:
            edges[a] = []
        edges[a].append(b)
        if b not in edges:
            edges[b] = []
        edges[b].append(a)

    leaves = [k for k, v in edges.items() if len(v) == 1] 
    root = 1
    depth = {root: 0}

    def dfs(c, d):
        depth[c] = d
        for n in edges[c]:
            if n not in depth:
                dfs(n, d + 1)
    dfs(root, 0)
    max_depth = max(depth.values())
    
    out = str(len(leaves))
    for l in leaves:
        out += f' {l} {max_depth-depth[l]}'
    print(len(leaves), max_depth)

    r.sendline(out)

r.interactive()