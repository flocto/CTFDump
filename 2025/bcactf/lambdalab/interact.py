from pwn import remote
# nc challs.bcactf.com 41985
r = remote("challs.bcactf.com", 41985)

defs = []
for i in range(1, 201):
    rhs = "(f " * i + "x" + ")" * i
    defs.append(f"{i} = λf.λx.{rhs}")

defs.append("0 = λf.λx.x")

defs += [
    # "populate 0 200",
    "true = λx.λy.x",
    "false = λx.λy.y",
    "pred = λn.λf.λx.n (λg.λh.h (g f)) (λu.x) (λu.u)",
    "succ = λn.λf.λx.f (n f x)",
    "iszero = λn.n (λx.false) true",
    "cons = λa.λb.λf.f a b",
    "car = λp.p true",
    "cdr = λp.p false",
    "+ = λm.λn.λf.λx.m f (n f x)",
    "- = λm.λn.n pred m",
    # "- = λm.λn.pred m",
    "* = λm.λn.λf.m (n f)",
    # "Y = λf.(λx.f (x x)) (λx.f (x x))",
    # "fact = Y (λfac.λn.λacc.n (λk.fac (pred n) (* n acc)) acc)",
    # "factorial = λn.fact n 1",
    # "factorial = λn.iszero n 1 (* n (factorial (pred n)))",
    # "factorial = λn.(* n (factorial (pred n)))",
    "factorial = λn.succ n",
    # "factorial = λn.n (λf.λm.f (* (succ m) (f m))) (λm.m) n",
    "run (+ (+ (car (cdr (cons 1 (cons 125 2)))) (- (* 3 14) (factorial 0))) (cdr (cons 1 1)))"
]

defs = [
    b"test = populate 0 200",
]

for d in defs:
    r.sendline(d)

r.interactive(prompt="")