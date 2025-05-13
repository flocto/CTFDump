from typing import (Tuple)  # noqa: F401

import numpy as np

from web3 import Web3
from web3.auto import w3
from eth_account.messages import encode_defunct, _hash_eip191_message

from eth_keys import keys
from eth_keys.backends.native.ecdsa import (
    ecdsa_raw_recover,
    deterministic_generate_k,
)
from eth_keys.backends.native.jacobian import (
    fast_multiply,
    inv,
)

from eth_utils import (
    big_endian_to_int,
    int_to_big_endian,
)

import sympy
from fastecdsa.point import Point
from fastecdsa.curve import secp256k1
from fastecdsa import keys as ecdsa_keys

P = 2**256 - 4294968273
N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
G = Point(
    0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
    0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8,
    curve=secp256k1,
)

def sqrt(n, p):
    """
    Finds the minimum positive integer m such that (m*m) % p == n.
    """
    return min(sympy.ntheory.residue_ntheory.sqrt_mod(n, p, all_roots=True))