import sys
inp = open(sys.argv[1], 'r').read()
out = open('dump/out.lc', 'w')
num = set('(λf.λx.f (f x )))')

consts = {
    '0': 'λf.λx.x ',
    '1': 'λf.λx.f x ',
    '2': 'λf.λx.f (f x )',
    '3': 'λf.λx.f (f (f x ))',
    'True': 'λt.λf.t ',
    'False': 'λt.λf.f ',
    '*': '(λm.λn.λf.λx.m (n f )x )',
    '-': '(λm.λn.n (λn.λf.λx.n (λg.λh.h (g f ))(λu.x )(λx.x ))m )',
    '+': '(λm.λn.λf.λx.m f (n f x ))',
    'cmp': '''(λx.λy.(True)
((λn.n (λv.False)(True))
(-
x 
y )
)
(False)((λn.n (λv.False)(True))
(-
y 
x )
)(False))''',
}

for i in range(2, 256):
    consts[str(i)] = f'λf.λx.f {"(f " * (i - 1)}x {")" * (i - 1)}'

const_map = { v: k for k, v in consts.items()}

out_str = inp
for k, v in const_map.items():
    out_str = out_str.replace(k, v)
out.write(out_str + '\n')

out.close()