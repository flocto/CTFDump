def dec(s):
    return "".join(chr(ord(c) ^ 13) for c in s)

d = [
    "%$03R0R&R",
    "%$03R0 R&R",
    "%$03R0R'R",
    "%$03vRR0R6R0R(RRp",
    "%$03R0RSR",
    "%$03R",
    "%$03R0-RRR#RRVRP",
    "%$03R0RRR#R%R00R$",
    "%$03vRR0R6R0RRR#R%R++RR$p",
    "%$03RRR%$",
]

for i in d:
    print(dec(i))

t = ["^y\x7Fdcj", "]\x7Fb`d~h", "nbc~bah", "@lye"]
for i in t:
    print(dec(i))

print(dec("zdcibz&R"))