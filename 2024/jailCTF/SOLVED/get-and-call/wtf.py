from functools import _HashedSeq

x = _HashedSeq.__init__.__builtins__
print(x)
x.popitem()

print(_HashedSeq.__init__.__builtins__)