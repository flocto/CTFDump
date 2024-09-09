parts = open('parts.txt').read().split('\n\n\n\n')

out = b''
rep_list = [
    '\\x', ';', ',', '%', (',', '0x'), '0x',
    'SPECIAL',
    (',', '0x'), '0x',
    'SPECIAL',
    '0x', ';', ':', (',', '0x')
]

for i, part in enumerate(parts):
    if i < len(rep_list):
        part = part.replace('\n', '')
        if type(rep_list[i]) == tuple:
            for rep in rep_list[i]:
                part = part.replace(rep, '')
        else:
            if rep_list[i] == 'SPECIAL':
                print(part, 'SPECIAL')
                continue

            part = part.replace(rep_list[i], ' ')
            part = ''.join(p.zfill(2) for p in part.split())

        # print(part)
        out += bytes.fromhex(part)
    
    else:
        print(part[:50])

    
open('out.txt', 'wb').write(out)