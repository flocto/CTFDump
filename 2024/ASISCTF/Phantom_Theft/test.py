import hashlib

B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

def base58encode(data):
	if data[0] == 0:
		return "1" + base58encode(data[1:])
	x = sum([v * (256 ** i) for i, v in enumerate(data[::-1])])
	ret = ""
	while x > 0:
		ret = B58[x % 58] + ret
		x = x // 58
	return ret

def base58decode(s):
    ret = 0
    for i in range(len(s)):
        ret += B58.index(s[i]) * (58 ** (len(s) - 1 - i))
    return bytes.fromhex(f"{ret:x}")

address = '198?PZBEMGtqGyW?Rm?wXgFSnnXr?9?Ki'
privkey = '5HuZo9gvP?ib1f?vX6xKBeefpHEUuPDJzXgBV?GJjRLVW?5kS?i'