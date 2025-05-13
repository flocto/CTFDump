def xorshift128(state0, state1):
    s1 = state0
    s0 = state1
    state0 = s0
    s1 ^= s1 << 23 
    s1 &= 0xFFFFFFFFFFFFFFFF
    s1 ^= s1 >> 17
    s1 ^= s0
    s1 ^= s0 >> 26
    state1 = s1
    return state0 & 0xFFFFFFFFFFFFFFFF, state1 & 0xFFFFFFFFFFFFFFFF

class XorShift128:
    
    def __init__(self, state0, state1):
        # print(bin(state0)[2:].zfill(64), bin(state1)[2:].zfill(64))
        self.state0 = state0
        self.state1 = state1

    def next(self):
        self.state0, self.state1 = xorshift128(self.state0, self.state1)
        return self.state0 + self.state1
        # return self.state0

    def choice(self, l):
        # print(f'choosing from {len(l)}')
        return l[self.next() % len(l)]

