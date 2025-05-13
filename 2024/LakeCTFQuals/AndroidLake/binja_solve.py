from binaryninja import BinaryView, Type
import z3

flag = [z3.BitVec(f'flag_{i}', 8) for i in range(63)]

def signext(val):
    return z3.SignExt(24, val) # always 8 -> 32

def parse_func(bv: BinaryView, name):
    func = bv.get_functions_by_name(name)[0]
    arg1 = func.parameter_vars[0]
    buf = None
    for var in func.hlil.vars:
        if (var_defs := func.hlil.get_var_definitions(var)):
            if arg1 in var_defs[0].vars_read:
                buf = var
                break

    if buf is None:
        print("Failed to find buffer")
        return
    
    buf.type = Type.pointer(bv.arch, Type.char())

    ev = ''.join(token.text for token in list(func.hlil.instructions)[-2].tokens).split(' = ', 1)[1]
    ev = ev.replace(buf.name, 'flag')
    ev = ev.replace('sx.d', 'signext')
    ev = ev.replace('*flag', 'flag[0]') # special case
    # print(f"Return: {ev}")
    expr = eval(ev)
    return expr

if __name__ == "__main__":
    bv: BinaryView = bv
    onload = bv.get_function_at(0x000200d0)
    hlil = onload.hlil
    s = z3.Solver()

    for line in hlil.instructions:
        if line.tokens[-1].text.startswith('Java_com_lake_ctf'):
            name = line.tokens[-1].text
            expr = parse_func(bv, name)
            s.add(expr)
    
    if s.check() == z3.sat:
        m = s.model()
        print(''.join(chr(m[flag[i]].as_long()) for i in range(63)))
    else:
        print("Failed to solve")