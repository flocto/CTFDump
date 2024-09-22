from types import *
from _distutils_hack import shim

x = tuple
print(x, type(x))
# print(x)

def traits(x):
    for d in dir(x):
        try:
            s = eval(f'(tuple).{d}')
            print(d, s, type(s))
        except:
            pass

traits(x)

print(list.mro())

# fro(m types import GetSetDescriptorType, BuiltinFunctionType, BuiltinMethodType, WrapperDescriptorType

# print(traits(int.from_bytes))