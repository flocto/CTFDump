import cy
import inspect  

# print(dir(cy))
# print(dir(cy.QOOQOOQOOQOOOQ()))
# exit()

class fakeint(int):
    def __init__(self, dat: int, name=None):
        # print(f'fakeint({dat}, {name})')
        self.dat = int(dat)
        if name is None:
            self.name = hex(id(self))[-6:]
        else:
            self.name = name
    
    def debugprint(self, dat):
        print(f'[{self.name}] {dat}')

    def __add__(self, other):
        r = self.dat + other
        self.debugprint(f'__add__({other}) -> {self.dat} + {other} = {r}')
        return fakeint(r)
    
    def __sub__(self, other):
        r = self.dat - other
        self.debugprint(f'__sub__({other}) -> {self.dat} - {other} = {r}')
        return fakeint(r)
    
    def __mul__(self, other):
        r = self.dat * other
        self.debugprint(f'__mul__({other}) -> {self.dat} * {other} = {r}')
        return fakeint(r)

    def __xor__(self, other):
        r = self.dat ^ other
        self.debugprint(f'__xor__({other}) -> {self.dat} ^ {other} = {r}')
        return fakeint(r)
    
    def __and__(self, other):
        r = self.dat & other
        self.debugprint(f'__and__({other}) -> {self.dat} & {other} = {r}')
        return fakeint(r)
    
    def __lshift__(self, other):
        r = self.dat << other
        self.debugprint(f'__lshift__({other}) -> {self.dat} << {other} = {r}')
        return fakeint(r)

    def __rshift__(self, other):
        r = self.dat >> other
        self.debugprint(f'__rshift__({other}) -> {self.dat} >> {other} = {r}')
        return fakeint(r)
    
    def __eq__(self, other):
        r = self.dat == other
        self.debugprint(f'__eq__({other}) -> {self.dat} == {other} = {r}')
        return r

    def __ne__(self, other):
        r = self.dat != other
        self.debugprint(f'__ne__({other}) -> {self.dat} != {other} = {r}')
        return r
    
    def __repr__(self):
        return f'fakeint({self.dat})'

out = None
key_idxs = []

class fakelist(list):
    def __init__(self, dat, name=None):
        super().__init__(dat)
        if name is None:
            self.name = hex(id(self))[-6:]
        else:
            self.name = name

    def debugprint(self, dat):
        print(f'[{self.name}] {dat}')

    def __getitem__(self, index):
        global key_idxs
        self.debugprint(f'__getitem__({index}), {super().__getitem__(index)}')

        if self.name == 'key':
            key_idxs.append(index)

        return super().__getitem__(index)
    
    def __setitem__(self, index, value):
        self.debugprint(f'__setitem__({index}, {value})')
        return super().__setitem__(index, value)
    
    def copy(self):
        return fakelist(super().copy(), self.name)
    
    def __eq__(self, other):
        global out
        r = super().__eq__(other)
        self.debugprint(f'__eq__({other}) -> {super().__repr__()} == {other} = {r}')
        out = self
        return r

key = b'SyC10VeRf0RVer' # cy.QOOQOOQOOQOOOQ().get_key()

def ret_key(arg):
    print(f'ret_key({arg})')
    return fakelist([fakeint(x) for x in key], 'key')
    # return key

cy.QOOQOOQOOQOOOQ.get_key = ret_key

# D = fakeint(2654435769)
# import gc
# for obj in gc.get_objects():
#     # find D
#     if not isinstance(obj, fakeint) and isinstance(obj, int) and obj == 2654435769:
#         obj = D
#         print(obj)

enc = [4108944556, 3404732701, 1466956825, 788072761, 1482427973, 782926647, 1635740553, 4115935911, 2820454423, 3206473923, 1700989382, 2460803532, 2399057278, 968884411, 1298467094, 1786305447, 3953508515, 2466099443, 4105559714, 779131097, 288224004, 3322844775, 4122289132, 2089726849, 656452727, 3096682206, 2217255962, 680183044, 3394288893, 697481839, 1109578150, 2272036063] # extracted by equals

# print(len(enc))

test = b'SCTF{abcd1234ABCD5678efgh1234AA}'
# test = b'A'*32
# test = b'B'*32

dat = fakelist([fakeint(x) for x in test], 'dat')

print(cy.sub14514(dat))
print(key_idxs)