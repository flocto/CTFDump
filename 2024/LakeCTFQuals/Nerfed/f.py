class Flags:
    def __init__(s) -> None:
        s.__flag = 0

    def toggle(s, bit):
        s.__flag = s.__flag ^ (1 << bit)

    def set_bit(s, bit, value=1):
        if value != s.get_bit(bit):
            s.toggle(bit)

    def clear(s, bit):
        s.__flag = s.__flag & ~(1 << bit)

    def get_bit(s, bit):
        return 1 if s.__flag & (1 << bit)else 0

    def get_hash(s):
        return hash(s.__flag)

    def get_num(s):
        return s.__flag
    
    def __str__(s):
        return f"{s.__flag:016b}"[::-1]
    
    def __repr__(s):
        return f"{s.__flag:016b}"[::-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
