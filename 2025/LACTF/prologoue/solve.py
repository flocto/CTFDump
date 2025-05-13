enc = '''dr
dr
u
l
u
dl
d
dr
dr
l
u
l
dr
ur
lu
dr'''

mapping = '''u  0
ur 1
r  2
dr 3
d  4
dl 5
l  6
lu 7'''
mapping = {
    k: v
    for k, v in map(str.split, mapping.split('\n'))
}

dec = ''.join(mapping[x] for x in enc.split('\n'))
dec = int(dec, 8)
print(dec.to_bytes((dec.bit_length() + 7) // 8, 'big'))

x = 164 * 196751
x = int(str(x), 8)
print(x.to_bytes((x.bit_length() + 7) // 8, 'big'))

x = 89060890

w = 97623387

for d in range(10):
    y = int(str(d) + str(w))
    c = x * y
    c = str(c)[::-1]
    # print(c, len(c))
    try:
        c = int(c, 8)
        print(c.to_bytes((c.bit_length() + 7) // 8, 'big'))
    except:
        pass

x = '5 -1 0 -3 1 2 -6 2 5 -1 0 -5 0 5 -4 1 1 0 3 -6 0 6 -2'
x = map(int, x.split())

arr = [2]
for i in x:
    arr.append(arr[-1] + i)

# print(len(arr))
# print(''.join(map(str, arr)))


x = 0o276634602766116234471175
print(x.to_bytes((x.bit_length() + 7) // 8, 'big'))