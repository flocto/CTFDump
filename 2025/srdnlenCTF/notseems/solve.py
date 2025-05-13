enc = b'32$.,%.;.s6s2\x1f425u4\x1f\x14(s\x1f-tq.\x1f&5.#4qp.='
dec = bytes([e ^ 0x40 for e in enc])
print(dec.decode())