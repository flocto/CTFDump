def run_prog(state: str, prog: str):
    steps = 0
    assert " " not in state
    before_outer = None
    splitted = prog.splitlines(keepends=False)
    assert len(splitted) < 200, "too long code"
    while True:
        if before_outer == state:
            break
        before_outer = state
        for line in splitted:
            if len(line.strip()) == 0:
                continue
            statement = line.split(" ")
            if len(statement) == 1:
                if statement[0] == "@":
                    if before_outer != state:
                        break
            else:
                before = None
                while True:
                    if before == state:
                        break
                    before = state
                    state = state.replace(statement[0], statement[1])
                    steps += 1
                    assert steps < 10000, "too many steps"
                    assert len(state) < 4000, "too many state"
    return state

prog = '''a 1
b 2
c 3'''
state = "abc"

print(run_prog(state, prog)) # 123

# from random import randint

# for _ in range(60):
#     a, b = randint(1, 1000), randint(1, 1000)
#     if a < 128 and b < 128:
#         print(a, b)