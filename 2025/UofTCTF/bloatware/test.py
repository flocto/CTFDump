import z3
s = z3.Solver()

inp = [z3.BitVec(f'flag_{i}', 8) for i in range(0x79d)]
for i in range(0x79d):
    s.add(z3.And(32 <= inp[i], inp[i] <= 127))
k = 0x27847c9d
inp.append(250297294)

data = open('wtf.txt').read().replace('_0x2a129d', 'inp')
data = eval(data)
print(len(data))

s.add(*data)

print(s.check())
