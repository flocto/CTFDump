import yaml
import string
import re
from collections import deque

yml = open('rules.yml', 'r')
rules = yaml.load(yml, Loader=yaml.FullLoader)['routes']

subs = {}
edges = {}
starts = {}
ends = set()

def parse_front(s):
    # (a)(b)(c)
    r = r'\((.)\)\((.)\)\((.)\)'
    m = re.match(r, s)
    if m:
        return ''.join(m.groups())
    return None

for rule in rules:
    if 'redirect' in rule:
        if 'regex_rewrite' in rule['redirect']:
            # print(rule['redirect']['regex_rewrite'])
            rule = rule['redirect']['regex_rewrite']

            regex = rule['pattern']['regex'][5:]
            regex = regex.replace('\-', '-') # ?

            sub = rule['substitution'][2:]
            
            if not sub or any([c in regex for c in '%_)']):
                subs[regex] = ''
                continue

            assert regex[0] == '/'
            regex = regex[1:]
            
            assert sub[-1] == '/'
            sub = sub[:-1]

            if sub[0] in string.ascii_lowercase:
                # print(f"{regex} -> {sub}")
                start = sub[0]
                rest = sub[1:]
                if start not in starts:
                    starts[start] = []
                starts[start].append(rest)
                # print(f'start: {start} -> {rest}')

                subs[regex] = start + rest
                
            elif sub[-1] not in string.ascii_uppercase:
                # print(f"{regex} -> {sub}")
                end = parse_front(sub)
                # print(f'end: {end}')
                ends.add(end)

                subs[regex] = end

            else:
                front, back = sub[:-3], sub[-3:]
                assert all([c in string.ascii_uppercase for c in back])
                front = parse_front(front)
                if front not in edges:
                    edges[front] = []
                edges[front].append(back)

                subs[regex] = front + back

inv_subs = {v: k for k, v in subs.items()}

# print(subs)
# print(edges)
# print(starts)
# print(ends)

flag = []
for c in 'tsgctf':
    q = deque()
    for start in starts[c]:
        q.append((start, [inv_subs[c + start]]))

    print(q)

    while q:
        c, path = q.popleft()
        s = c.lower()[::-1]
        if s in ends:
            part = ''.join(path + [inv_subs[s]])
            print(c, part)
            flag.append(part)
            break

        last_path = path[-1]
        if s in edges:
            for edge in edges[s]:
                if last_path + inv_subs[s + edge] in subs:
                    continue # edge case
                q.append((edge, path + [inv_subs[s + edge]]))

        # print(q)
        # input()

print('_'.join(flag[::-1])) 