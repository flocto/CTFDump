import dis
from opcode import opmap

def o(name):
    return opmap[name]

def run():
    pass

def test():
    a = 1
    print(a)

c = test.__code__
for inst in dis.Bytecode(c):
    print(inst, inst.opname)
print("===")

# for i in range(256):
#     try:
#         code = bytes(
#             [
#                 # o('BUILD_LIST'), 0,
#                 # o('UNPACK_SEQUENCE'), 2,
#                 # # o('POP_JUMP_IF_FALSE'), 1,
#                 # o('RETURN_VALUE'), 0,
#                 i, 0,
#                 # o('PRINT_EXPR'), 0,
#             ]
#         )
#         print(list(code))

#         names = ('builtins', 'builtins', 'builtins', 'builtins', 'builtins')
#         c = run.__code__.replace(co_code=code, co_names=names)
#         for inst in dis.Bytecode(c):
#             if (
#                 inst.opname.startswith("LOAD")
#                 or inst.opname.startswith("STORE")
#                 or inst.opname.startswith("IMPORT")
#             ):
#                 print(f"Invalid op {inst.opname}")
#                 # exit()
#             else:
#                 print(inst, inst.opname)

#         run.__code__ = c
#         print(run())
#     except:
#         print("Error", i)
#         continue

code = bytes(
    [
        # o('BUILD_LIST'), 0,
        # o('UNPACK_SEQUENCE'), 2,
        # # o('POP_JUMP_IF_FALSE'), 1,
        # o('RETURN_VALUE'), 0,
        o('EXTENDED_ARG'), 255,
        o('JUMP_ABSOLUTE'), 255,
        o('BUILD_STRING'), 0,
        o('PRINT_EXPR'), 0,
        o('RETURN_VALUE'), 0,
    ]
)
print(list(code))

names = ('builtins', 'builtins', 'builtins', 'builtins', 'builtins')
c = run.__code__.replace(co_code=code, co_names=names)
for inst in dis.Bytecode(c):
    if (
        inst.opname.startswith("LOAD")
        or inst.opname.startswith("STORE")
        or inst.opname.startswith("IMPORT")
    ):
        print(f"Invalid op {inst.opname}")
        exit()
    else:
        print(inst, inst.opname)

run.__code__ = c
print(run())