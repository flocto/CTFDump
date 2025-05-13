class LCG:
    def __init__(self, seed, a, c, m):
        self.seed = seed
        self.a = a
        self.c = c
        self.m = m

    def next(self):
        self.seed = (self.a * self.seed + self.c) % (self.m)
        return self.seed

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()
    
    def prev(self):
        self.seed = (self.seed - self.c) * pow(self.a, -1, self.m) % (self.m)
        return self.seed
    
# long m = 1L << 52;
# long c = 4164880461924199L;
# long a = 2760624790958533L;
# seed = (a *seed+ c) & (m -1L);
    
a = 2760624790958533
c = 4164880461924199
m = 1 << 52
x = 4233483945265577
I = 3473400794307473
low = int(m/10*9)
data = '''[x = 4110811103746190] 4110811103746190
[x = 4458516016761798] 4458516016761798
[x = 4408706512728006] 4408706512728006
[x = 4062623185186385] 4062623185186385
[x = 4087494368585084] 4087494368585084
[x = 4177966339412008] 4177966339412008
[x = 4323905945053229] 4323905945053229
[x = 4344807263526324] 4344807263526324
[x = 4430332399956968] 4430332399956968'''

data = '''4211908915791827
4454353724525538
4218970610864145
4111556049211198
4125745731590009
4458744023838989
4479821434387034'''

# data = open('dump.txt').read()

data = '''4359404241011232
4337090406850605'''
for line in data.splitlines():
    x = int(line.split()[-1])
    lcg = LCG(x, a, c, m)
    for i in range(26):
        t = lcg.prev()
    print(t ^ I, lcg.prev() ^ I)
    
        



