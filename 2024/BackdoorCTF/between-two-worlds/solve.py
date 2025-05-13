class MT19937:
    """Classical Mersenne Twister Implementation."""

    def __init__(self, seed=None):
        self.mt = [0 for i in range(624)]
        self.index = 624
        if seed is not None:
            self.seed(seed)

    def seed(self, seed):
        self.mt[0] = seed
        for i in range(1, 624):
            self.mt[i] = self._int32(0x6c078965 *
                                (self.mt[i - 1] ^ (self.mt[i - 1] >> 30)) + i)

    def extract(self):
        """ Extracts a 32bit word """
        if self.index >= 624:
            self.twist()

        x = self.mt[self.index]
        x ^= x >> 11
        x ^= (x << 7) & 0x9d2c5680
        x ^= (x << 15) & 0xefc60000
        x ^= x >> 18

        self.index += 1
        return self._int32(x)

    def twist(self):
        """ The twist operation. Advances the internal state """
        for i in range(624):
            upper = 0x80000000
            lower = 0x7fffffff

            x = self._int32((self.mt[i] & upper) +
                            (self.mt[(i + 1) % 624] & lower))
            self.mt[i] = self.mt[(i + 397) % 624] ^ (x >> 1)

            if x & 1 != 0:
                self.mt[i] ^= 0x9908b0df

        self.index = 0

    def _int32(self, x):
        return x & 0xffffffff
    
    def randbytes(self, n):
        return bytes([self.extract() & 0xff for _ in range(n)])
    
seed = 1734847507

r = MT19937(seed)

key = r.randbytes(16)
iv = r.randbytes(16)
print(key.hex())
print(iv.hex())

key = bytes([k ^ 152 for k in key])
iv = bytes([i ^ 152 for i in iv])
print(key.hex())
print(iv.hex())