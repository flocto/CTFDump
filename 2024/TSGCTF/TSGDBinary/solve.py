import struct
def xor(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

enc = bytes.fromhex('08091d55571918175408510119181551474841414644454608004e5b564109425f4d5114415d5141446b571f0c51175d')
pt = b'A' * 0x30
key = xor(enc, pt)

targets = [7359478011354880797, 2333770859931840375, 7738690943358031476, 7212289551246586236, 7084013153596436090, 2041939551910839348]
targets = struct.pack('<' + 'Q' * len(targets), *targets)

print(xor(key, targets))