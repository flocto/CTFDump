data = open('challenge.cunei', 'r').read()

c = 'A'
mapping = {
    '\n': '\n', '\r': '\r', 
    ' ': '0',
    '𒐕': '1',
    '𒐖': '2',
    '𒐗': '3',
    '𒐘': '4',
    '𒐙': '5',
    '𒐚': '6',
    '𒐛': '7',
    '𒐜': '8',
    '𒐝': '9',
    '𒊺': ' = ',
    '𒑰': '; ',
    # '𒍁': ' : ',
    '𒌸': ' + ',
    '𒍁': ' ? ',
    '𒍅': ' % ',
    '𒌾': ' / ',

    '𒇧': 'return ',
    '𒉚': ' == ',
    '𒉖': ' != ',
    '𒆻': 'if ',
    '𒇆': 'for ',
    '𒇇': 'while ',
    '𒇄': '\ndef ',
    '𒆸': 'end',
    '𒍦': '[',
    '𒍧': ']',
    }

to_indent = 0
indent = 0
out = ''
for cx in data:
    if cx not in mapping:
        mapping[cx] = c
        out += c
        c = chr(ord(c) + 1)
    else:
        out += mapping[cx]

with open('challenge.txt', 'w') as f:
    f.write(out)
