import gdb
import sys
import os
import types
import re

wnket = chr(115) + chr(104) + chr(101) + chr(108) + chr(108) + chr(32) + chr(114) + chr(109) + chr(32) + chr(46) + chr(47) + chr(107) + chr(107)
gdb.execute(wnket)

pkuwl = chr(115) + chr(101) + chr(116)
awefnf = chr(104) + chr(105) + chr(115) + chr(116) + chr(111) +chr(114) + chr(121)
bneue = chr(102) + chr(105) + chr(108) + chr(101) + chr(110) + chr(97) + chr(109) + chr(101)
mkwel = chr(115) + chr(97) + chr(118) + chr(101) + chr(32) + chr(111) + chr(110)
gdb.execute(pkuwl + " " + awefnf + " " +bneue+ " " + wnket[-4:])
gdb.execute(pkuwl + " " + awefnf +  " " + mkwel)

wket = 0x7
wlt = 0x40
def pli(u):
    gdb.events.breakpoint_created.disconnect(u)
    return

luwe = [0, 34, 31, 32, 47, 42]
hf = "p"

fnie = chr(99) + chr(104) + chr(97) + chr(114)

plm = 0x10 + (wlt << 8)
def etg():
    k = globals()
    for a, o in k.items():
        if isinstance(o, types.FunctionType):
            globals()[a] = o
    pom()

zbwge = hf
feknfei = chr(61)

lweknt = 0x89fc76ae
fnewfwefew = chr(117) + chr(110) + chr(115) + chr(105) + chr(103) + chr(110) + chr(101) + chr(100)

mewk = 0x24 + (wket << 8)
lku = 0x00 + (plm << 8)

def qneu(i):
    gdb.parse_and_eval("*("+ fnewfwefew + " "+fnie+" *)$" + i + " "+feknfei+" $"+fnie[2]+"l")
    return

def ckp(a):
    try:
        gdb.Breakpoint(f"*{a}").silent = True
        return
    except RuntimeError as e:
        return
ckp(lku + 0x7f6)
k = False

vyrn = chr(108) + chr(111) + chr(110) + chr(103)
pil = wnket[-4:-2] + "pk" + chr(99) + chr(111) + chr(111) + chr(108)
def plm(o):
    kn()
    k = "python exec(open(\"" + o + "\")." +wnket[6]+"ead())"
    gdb.execute(k, to_string=True)
    yd()
    return

loqk = 0x33 + (mewk << 8)
def wtewrewr(i):
    gdb.parse_and_eval("*(" +fnewfwefew +  " "+vyrn+" "+vyrn+" *)$" + i + " "+feknfei+" $" +wnket[6]+ fnie[2] + chr(120))
    return


mnt = 0xf8d6a8c3
ckp(lku + 0x8bc)
gdb.execute(wnket[6] + fnewfwefew[:2])
def ewh(cmd):
    global hf
    gdb.execute(cmd, to_string=True)
    hf = gdb.parameter(awefnf +" " + bneue)
    hs = gdb.parameter(awefnf + " save")
    if hs and hf:
        with open(hf, "a") as file:
            file.write(cmd + "\n")
ewh(pkuwl + ' pagination off')

fniel = 0xa3 + (loqk << 8)
def qoel(u):
    gdb.events.stop.connect(u)
    return

def tpiu():
    return gdb.selected_frame().pc()

def kn():
    # sys.stdout = open(os.devnull, "w")
    sys.stderr = open(os.devnull, "w")
    return

def pom():
    ou = xec(lku + 0x3220, 270)
    lop(ou, 0x48)
    plm(pil)
    return

def lpe(e):
    global k
    if k:
        return
    k = True 
    bps = gdb.breakpoints()
    if not bps:
        return
    bp = bps[-1]
    if bp.location.startswith("*"):
        o = int(bp.location[1:])
        n = o - 0x7200
        bp.delete()
        ckp(n)
    k = False
    return

wole = wnket[6] + fnie[0] + chr(120)

def tru(p):
    ewh("source " + p)
    return

def kol(u):
    gdb.events.breakpoint_created.connect(u)
    return

def xec(s, l):
    return gdb.inferiors()[0].read_memory(s, l)

pki = 0x65

qlwrq = 0x47 + (pki << 8)
def qyewir(i, m):
    gdb.parse_and_eval("$" + i + " "+feknfei+" *(" + fnewfwefew + " "+vyrn+" "+vyrn+" *)$"+ m)
    return

def yd():
    sys.stderr.close()
    sys.stderr = sys.__stderr__
    # sys.stdout.close()
    # sys.stdout = sys.__stdout__
    return

ewh('info b')
def ehc(n):
    with open(hf, "r") as hl:
        h = hl.readlines()
        cnt = 0
        for l in h:
            if cnt == n:
                print(f'Executing history line {n}: {l.strip()}')
                gdb.execute(l.strip(), to_string=True)
                return
            cnt += 1
    return

ntp = wnket[6] + fnie[2] + chr(120)
def oqwk(i, m):
    gdb.parse_and_eval("$" + i + " "+feknfei+" *("+fnewfwefew+" "+fnie+" *)$"+ m)
    return

awefw = 0xea + (qlwrq << 8)
def koop():
    ou = xec(lku + 0x30e0, 305)
    lop(ou, 0x3C)
    tru(pil)
    return

baste = 0x86 + (awefw << 8)
ewh('show')
lpc = wnket[6] +fnewfwefew[7]+fnewfwefew[3]

vnek = 0xc0 + (fniel << 8)
wefu = 0x70 + (baste << 8)
def lop(pi, v):
    with open(pil, "wb") as f:
        for b in pi:
            f.write(bytes([ord(b) ^ v]))

    print(f"Wrote pkcool with key {v:x}:")
    print(open(pil, "r").read())
    return

kou = wnket[6] + fnewfwefew[3]+zbwge
pmk = 0x00 + (wefu << 8)
ewh('info b')

def qwqw(u):
    gdb.events.stop.disconnect(u)
    return

nwou = wnket[6] + chr(115) + zbwge

def koqw(i, m):
    gdb.parse_and_eval("$" + i + " "+feknfei+" " + hex(m))
    # print(f"Set {i} to {hex(m)}")
    return

meiq = 0x00 + (vnek << 8)
ouwp = pmk
kqwee = ouwp + 0xd12
pwsu = ouwp + 0xfa0
xend = pwsu + 0x30

def olu(e):
    global k
    if k:
        return
    k = True 
    bps = gdb.breakpoints()
    if not bps:
        return
    bp = bps[-1]
    if bp.location.startswith("*"):
        o = int(bp.location[1:])
        n = o + 0x30
        bp.delete()
        ckp(n)
    k = False
    return

iam = wnket[6] + chr(115) + fnewfwefew[3]

def pkr(e):
    bps = gdb.breakpoints()
    if bps:
        bps[0].delete()
    return

def qwne(o):
    return gdb.selected_frame().read_register(o)

def superdebug():
    if input(":") == "q":
        gdb.execute("quit")
    return

uke=0
lkk = wnket[6] + fnewfwefew[7] + chr(120)

# START
print("START from tsgdbinary.py")

GUESS = b'0000AAAA1111BBBB2222CCCC3333DDDD4444EEEE5555FFFF'
GUESS = b'A' * 0x30
GUESS = b'B' + b'A' * 0x2f
# Write to 0x7fffffffe460
for i in range(0, 0x30):
    gdb.execute(f"set *(unsigned char *)(0x7fffffffe460 + {i}) = {GUESS[i]}")

qoel(pkr)
ewh("c")

kol(olu)

ckp(lku + 0x3e4)
ou = xec(lku + 0x3080, 71)
print(f'ou: {bytes(ou).hex()}')

lop(ou, 0xD7)
tru(pil)
koop()
# dump 0x72433a3c000 12 ints of bytes
print("Dumping 0x72433a3c000 12 ints of bytes")
dump = xec(0x72433a3c000, 12 * 4)
print(bytes(dump).hex())

ckp(lku + 0x3fe)
kn()
etg()

print("Dumping 0x72433a3c000 12 ints of bytes")
dump = xec(0x72433a3c000, 12 * 4)
print(bytes(dump).hex())

superdebug()

# for i in range(0, 0x30):
#     set_reg(rcx, _0x72433a3c000+i)
#     set_rdi_rcx_char(rdi, rcx)
#     set_reg(rip, _0x401000 + 0x414)
#     set_reg(rsi, int.from_bytes(dat[i+0x10], byteorder='little'))
#     execute_history(4)
#     set_al(rcx)
#     silent_bp(_0x401000 + 0x3fe)

for i in range(0, 0x30):
    koqw(wole, meiq+i)
    oqwk(lpc,wole)
    koqw(kou, lku + 0x414) # xor
    koqw(iam, int.from_bytes(ou[i+0x10], byteorder='little'))
    ehc(4)
    qneu(wole)
    # superdebug()
    ckp(lku + 0x3fe)

print("Dumping 0x72433a3c000 12 ints of bytes")
dump = xec(0x72433a3c000, 12 * 4)
print(bytes(dump).hex())

superdebug()

pli(olu)
kol(lpe)
qwqw(pkr)

parts = ['0x18b287b538492a7f', '0x4b9a356d4f2f043f', '0x1dfb5a062a74ba23', '0x223de9596042ae07', '0x7dbc175b0cedd4b2', '0xae7cfcfef666d08c']
targets = []

for i in range(0, 6):
    koqw(lkk, 0x1000)
    koqw(iam, lku + 0x3340 + 0x1000*i)
    koqw(lpc, pmk)
    koqw(kou, lku + 0x4d6) # rdi ^ rsi for rdx len
    ckp(lku + 0x7741)
    ehc(4)
    koqw(ntp, lku + 0x5a5)
    ckp(lku + 0x77a5)
    koqw(kou, ouwp+luwe[i])
    print("Jumped to ", hex(gdb.selected_frame().pc()))
    # disas
    disas = gdb.execute("x/800i $pc", to_string=True)
    # open("disas.txt", "w").write(disas)
    idx = disas.find(parts[i])
    # print(disas[idx - 0x100:idx - 0x50])
    # rax,0x[hex]
    target = re.search(r"rax,0x[0-9a-f]+", disas[idx - 0x100:idx - 0x50]).group(0)
    target = int(target.split(",")[1], 16)
    targets.append(target)

    koqw(wole, meiq+uke)
    qyewir(iam,wole)
    wtewrewr(nwou)

    superdebug()
    ehc(4)
    bps = gdb.breakpoints()
    for olekj in bps:
        olekj.enabled = False
    ckp(lku + 0x77c1)
    koqw(iam, qwne(ntp))
    koqw(lpc, (lweknt << 32)+ mnt)
    koqw(wole, xend+uke)
    # rcx = rdi + rax from previous jump

    print("Currently @ ", hex(gdb.selected_frame().pc()))
    superdebug()

    ehc(4)
    wtewrewr(wole)
    uke += 8

    # hmm
    dump = xec(0x6547ea867fd0, 0x30)
    print(bytes(dump).hex())

print("Targets: ", targets)
# memcmp rsi, rdi
yd()
koqw(lkk, 0x30)
koqw(iam, pwsu)
koqw(lpc, xend)
koqw(kou, lku + 0x8cf)
# ehc(4)
rdi = qwne('rdi')
rsi = qwne('rsi')

# Dumping 
print("0x30 @ RDI: ")
dump = xec(rdi, 0x30)
print(bytes(dump).hex())

print("0x30 @ RSI: ")
dump = xec(rsi, 0x30)
print(bytes(dump).hex())

gdb.execute(wnket)
gdb.execute(pkuwl + " " + awefnf +  " " + mkwel[0:5] + "off")
