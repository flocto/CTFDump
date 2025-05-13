#!/usr/bin/env python3
import numpy as np


class T:
    npz = np.load("tz.npz")
    compute_check = npz["compute_check"]
    compute_check.flags.writeable = False
    compute_hash = npz["compute_hash"]
    compute_hash.flags.writeable = False
    flag_check = npz["flag_check"]
    flag_check.flags.writeable = False
    flag_hash = npz["flag_hash"]
    flag_hash.flags.writeable = False
    reg_check = npz["reg_check"]
    reg_check.flags.writeable = False
    reg_hash = npz["reg_hash"]
    reg_hash.flags.writeable = False
    masks = npz["masks"]
    masks.flags.writeable = False
    reg_scrable = npz["reg_scrable"]
    reg_scrable.flags.writeable = False
# Created by pyminifier (https://github.com/liftoff/pyminifier)
