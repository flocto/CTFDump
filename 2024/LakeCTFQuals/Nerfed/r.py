class Registers:
    def __init__(s) -> None:
        s.__r = [0 for _ in range(11)]

    def set(s, r, v):
        s.__r[r] = v

    def get(s, r):
        return s.__r[r]

    def get_hash(s):
        return s.__r
# Created by pyminifier (https://github.com/liftoff/pyminifier)
