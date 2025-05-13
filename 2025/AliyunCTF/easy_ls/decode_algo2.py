def decode_algo2(text: str, cnt = 0):
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

def encode_algo2(text: str, cnt = 0):
    offset = 12 + cnt
    enc = ""
    for c in text:
        if c.islower() and c.isalpha():
            enc += chr((ord(c) - 97 + offset) % 26 + 97)
        elif c.isupper() and c.isalpha():
            enc += chr((ord(c) - 65 + offset) % 26 + 65)
        elif c.isdigit():
            enc += str((int(c) + offset) % 10)
        else:
            # this should not happen
            enc += c
    
    return enc

enc = 'QkInJFLrVcOonxxd'
print(decode_algo2(enc, 6))
