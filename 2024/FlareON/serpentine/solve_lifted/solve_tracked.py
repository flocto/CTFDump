import re
from z3 import *
set_param("parallel.enable", True)
# from cvc5.pythonic import *

tracked_ops = open('tracked_ops.txt').read().splitlines()
op_dict = {
    'add': '+',
    'sub': '-',
    'xor': '^',
}

def parse_term(term):
    inbetween_op = None
    if term[0] != '(':
        inbetween_op = term[0]
    term = term[term.find('('):].rsplit(' ', 2)
    inner = term[0][1:-1].split(' -> ')[0]
    op = op_dict[term[1]]
    const = term[2]

    # print(inner, op, const, inbetween_op)
    return inner, op, const, inbetween_op

s = Solver()
flag = [BitVec(f'flag_{i}', 64) for i in range(0x20)]
for f in flag:
    s.add(f >= 32, f <= 126)

for line in tracked_ops:
    terms, last_const = line.rsplit(' ', 1)
    terms = terms[1:-1].split(', ')
    # print(terms, const)
    eq = ''
    for term in terms:
        inner, op, const, inbetween_op = parse_term(term)
        if inbetween_op:
            eq = f'({eq} {inbetween_op} {inner})'
        else:
            eq = inner
        eq = f'({eq} {op} {const})'
    # print(f'{eq} = {last_const}')
    eq += f' - {last_const}'

    # print(eq)
    s.add(eval(eq) == 0)

if s.check() == sat:
    m = s.model()
    print(''.join([chr(m[f].as_long()) for f in flag]))