#!/usr/local/bin/python3

import pickle
import pickletools
from io import BytesIO
from ast import literal_eval

user_data = int(input('favorite number > '))
flag = open('flag.txt').read().strip()
dumped = pickle.dumps((user_data, flag))

print(dumped)
pickletools.dis(dumped)

assert len(flag) == 79, len(flag)

dumped = bytearray(dumped)
dumped[int(input('radiation alert! > ')) % len(dumped)] += 1
dumped = bytes(dumped)

print(dumped)
pickletools.dis(dumped)

class ActuallySecureUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        return 'no'

info, _ = ActuallySecureUnpickler(BytesIO(dumped)).load()
print(f'here is your info: {info}')

