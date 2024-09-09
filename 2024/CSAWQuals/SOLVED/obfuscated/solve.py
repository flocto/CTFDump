import gdb
import string

alpha = ' ' + string.ascii_lowercase + string.digits + string.ascii_uppercase + string.punctuation
known = 'wh47 15 7h3 r1ck 457l3y p4r4d0x?' # done
known = '' # ^

def test(inp):
    open('input.txt', 'w').write(inp)
    gdb.execute('run < input.txt') # look theres like punctuation and stuff so i dont want to bother with shell escaping
    print(inp)

    for _ in range(len(inp) - 1):
        # eax = int(gdb.parse_and_eval('$eax'))
        # ecx = int(gdb.parse_and_eval('$ecx'))
        # print(hex(eax), hex(ecx), inp[i])
        gdb.execute('c')

    eax = int(gdb.parse_and_eval('$eax'))
    ecx = int(gdb.parse_and_eval('$ecx'))

    if eax == ecx:
        print('Match:', inp)
        return True

# brva 0x000297ad has sidechannel
# commands 1
# silent
# end

while True:
    for c in alpha:
        if test(known + c):
            known += c
            print('Known:', known)
            break