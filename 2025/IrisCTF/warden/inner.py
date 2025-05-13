import sys
import os
import inspect
import seccomp
from {a} import {b} as win

for k in list(sys.modules):
    del sys.modules[k]
while len(sys.meta_path) > 0:
    del sys.meta_path[0]
for k in list(sys.path_importer_cache):
    del sys.path_importer_cache[k]
sys.builtin_module_names = ()

f = inspect.currentframe()

filter = seccomp.SyscallFilter(seccomp.ALLOW)
action = seccomp.KILL
filter.add_rule(action, "execve")
filter.add_rule(action, "execveat")
filter.add_rule(action, "vfork")
filter.add_rule(action, "fork")
filter.load()

sys.addaudithook((lambda x: lambda *_: print('audit hit') | x(-1))(os._exit))

for k in f.f_builtins:
    f.f_builtins[k] = None
for k in f.f_globals:
    if k != "f" and k != "win":
        f.f_globals[k] = None
for k in f.f_locals:
    if k != "f" and k != "win":
        f.f_locals[k] = None
del f
del k

win({repr(arg)})