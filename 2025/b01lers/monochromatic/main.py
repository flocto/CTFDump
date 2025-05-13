#!/usr/local/bin/python3
import dis
import gc


def run():
    pass


gc.disable()
inp = bytes.fromhex(input("Bytecode: "))
names = tuple(input("Names: ").split())
if len(inp) > 200:
    print(f"Invalid bytecode {inp}")
    exit()
if len(names) > 5:
    print(f"Invalid names {names}")
    exit()
code = run.__code__.replace(co_code=inp, co_names=names)
for inst in dis.Bytecode(code):
    if (
        inst.opname.startswith("LOAD")
        or inst.opname.startswith("STORE")
        or inst.opname.startswith("IMPORT")
    ):
        print(f"Invalid op {inst.opname}")
        exit()
run.__code__ = code
run()