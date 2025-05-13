enc = '6JJgKGNErps8zJM93aJpL2AhqXbjUTTDkWwf3UVuz3GwFu1jkonQVhsN9h39QVuzTFSDA3YGjTtDyGXjF1ZwwpoBKab2vvCf6kdb1Ms9Ams2Hri9ppzomNKBD5ScoRwszTnqTZkEBw46XfLJmsnirLr3sJ3SCi26Fa36Eq3sq4bNCAtG8yAMpqxfsp7ob81Qwt6e2WtCuLUepEqN8eew79Naq5bRXWQhr9XCtBmPuiSSdNERh3p6XbARTnP9FfcvMivjhRquSw3TXvzAYiahsdBsPtFR5KLVsXtsGcXbReWowvu5GMt6Y3'

base58_alpha = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
def algo1_decode(s):
    s = s[:-1]
    result = 0
    for c in s:
        result *= 58
        # print(c)
        result += base58_alpha.index(c)
    return result.to_bytes((result.bit_length() + 7) // 8, 'big').decode()

def algo2_decode(text: str):
    global cnt
    offset = 12 + cnt
    dec = ""
    for c in text[:-1]:
        if c.islower() and c.isalpha():
            dec += chr((ord(c) - 97 - offset) % 26 + 97)
        elif c.isupper() and c.isalpha():
            dec += chr((ord(c) - 65 - offset) % 26 + 65)
        elif c.isdigit():
            dec += str((int(c) - offset) % 10)
        else:
            # this should not happen
            dec += c
    
    return dec

def algo3_decode(s):
    return s[:-1][::-1]

cnt = 47
decodes = [algo1_decode, algo2_decode, algo3_decode]
dec = ''

while cnt > 0:
    decs = {}
    for i in range(3):
        try:
            *rest, last = decodes[i](enc)
            decs[i] = (rest, last)
        except Exception as e:
            print(e)
    
    for i, (rest, last) in decs.items():
        print(i, last)
    
    idx = int(input('> '))
    rest, last = decs[idx]
    dec = last + dec
    enc = ''.join(rest)
    cnt -= 1
    print(dec)
