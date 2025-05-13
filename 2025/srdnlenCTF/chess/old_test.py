from src.encode_to_pgn_2bit import encode_to_pgn, bits_to_string
from src.trivia import trivia
from src.pseudorandom import XorShift128
import secrets 

s = '01110010'
SIZE = 64
prng = XorShift128(secrets.randbits(SIZE), secrets.randbits(SIZE))

for i in range(1):
    print(encode_to_pgn(bits_to_string(s), prng))