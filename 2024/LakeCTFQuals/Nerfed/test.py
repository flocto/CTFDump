#!/usr/bin/env python3
# import numpy as np

# npz=np.load("tz.npz")

# for key in npz.keys():
#     print(key, npz[key].shape, npz[key].dtype)

import itertools
from tqdm import tqdm
import main
start = b'\x00' 

for p in tqdm(list(itertools.product(range(256), repeat=2))):
    if any(x == 254 for x in p):
        continue
    payload = start + bytes(p[0:1]) + b'\x19' + bytes(p[1:2])

    main.comp_passed = 0
    main.reg_passed = 0
    x = main.main(payload)
    # print(p, x, main.comp_passed, main.reg_passed)
    if main.comp_passed == 2:
        print(p, x, main.comp_passed, main.reg_passed)
