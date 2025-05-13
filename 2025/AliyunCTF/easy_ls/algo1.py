base58_alpha = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def base58_encode(s):
    result = ''
    n = int.from_bytes(s.encode(), 'big')
    while n > 0:
        n, r = divmod(n, 58)
        result = base58_alpha[r] + result
    return result

def base58_decode(s):
    s = s[:-1]
    result = 0
    for c in s:
        result *= 58
        result += base58_alpha.index(c)
    return result.to_bytes((result.bit_length() + 7) // 8, 'big').decode()

s = 'YsQvRNTzDkWwvff'
e = '3W9ZwHdNUy6yGiymcuirya'

print(base58_encode(s), e)
print(base58_decode(e), s) 

e = '38a'
print(base58_decode(e))