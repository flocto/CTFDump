import gdb
import sys
import os
import types

shell_rm = 'shell rm ./kk'
gdb.execute(shell_rm)

set_ = 'set'
history_ = 'history'
filename_ = 'filename'
save_on_ = 'save on'
gdb.execute(set_ + " " + history_ + " " + filename_ + " " +
            shell_rm[-4:])  # set history filename ./kk
gdb.execute(set_ + " " + history_ + " " + save_on_)  # set history save on

_7 = 7
_64 = 0x40



def remove_breakpoint_listener(u):
    gdb.events.breakpoint_created.disconnect(u)
    return


idxs = [0, 34, 31, 32, 47, 42]
p = "p"

char = 'char'

_0x4010 = 0x10 + (_64 << 8)


def weird_globals_run_py():
    for a, o in globals().items():
        if isinstance(o, types.FunctionType):
            globals()[a] = o
    read_and_run_py_pkcool()


_p = p
_eq = '='

_0x89fc76ae = 0x89fc76ae
unsigned = 'unsigned'

_0x724 = 0x24 + (_7 << 8)
_0x401000 = 0x00 + (_0x4010 << 8) # 0x401000


def set_al(addr):
    gdb.parse_and_eval("*(unsigned char *)$" + addr + " = $al")
    return


def silent_bp(addr):
    try:
        gdb.Breakpoint(f"*{addr}").silent = True
        return
    except RuntimeError as e:
        return


silent_bp(_0x401000 + 0x7f6)
kflag = False

long = 'long'
_pkcool = './pkcool'

def run_py_file(fn):
    redirect_null()
    k = "python exec(open(\"" + fn + "\").read())"
    gdb.execute(k, to_string=True)
    reset_output_streams()
    return


_0x72433 = 0x33 + (_0x724 << 8)

def set_addr_to_rax(addr):
    gdb.parse_and_eval("*(unsigned long long *)$" + addr + " = $rax")
    return


_0xf8d6a8c3 = 0xf8d6a8c3
silent_bp(_0x401000 + 0x8bc)
gdb.execute('run')


def execute_and_log_command(cmd):
    global p
    gdb.execute(cmd, to_string=True)
    p = gdb.parameter(history_ + " " + filename_)
    hs = gdb.parameter(history_ + " save")
    if hs and p:
        with open(p, "a") as file:
            file.write(cmd + "\n")

execute_and_log_command(set_ + ' pagination off')

_0x72433a3 = 0xa3 + (_0x72433 << 8)


def register_stop_handler(u):
    gdb.events.stop.connect(u)
    return


def current_frame_pc():
    return gdb.selected_frame().pc()


def redirect_null():
    sys.stdout = open(os.devnull, "w")
    sys.stderr = open(os.devnull, "w")
    return


def read_and_run_py_pkcool():
    ou = read_memory(_0x401000 + 0x3220, 270)
    write_pkcool(ou, 0x48)
    run_py_file(_pkcool)
    return


def update_breakpoint(e):
    global kflag
    if kflag:
        return
    kflag = True
    bps = gdb.breakpoints()
    if not bps:
        return
    bp = bps[-1]
    if bp.location.startswith("*"):
        o = int(bp.location[1:])
        n = o - 0x7200
        bp.delete()
        silent_bp(n)
    kflag = False
    return


rcx = 'rcx'


def execute_script(p):
    execute_and_log_command("source " + p)
    return


def connect_breakpoint_handler(u):
    gdb.events.breakpoint_created.connect(u)
    return


def read_memory(addr, n):
    return gdb.inferiors()[0].read_memory(addr, n)


_0x65 = 0x65

_0x6547 = 0x47 + (_0x65 << 8)


def set_rsi_rcx_ll(i, m): # pretty sure this only happens to $rsi = *$rcx
    gdb.parse_and_eval("$" + i + " = *(unsigned long long *)$" + m)
    return


def reset_output_streams():
    sys.stderr.close()
    sys.stderr = sys.__stderr__
    sys.stdout.close()
    sys.stdout = sys.__stdout__
    return


execute_and_log_command('info b')


def execute_history(n):
    with open(p, "r") as hl:
        h = hl.readlines()
        cnt = 0
        for l in h:
            if cnt == n:
                gdb.execute(l.strip(), to_string=True)
                return
            cnt += 1
    return


rax = 'rax'


def set_rdi_rcx_char(i, m): # only happens rdi, rcx
    gdb.parse_and_eval("$" + i + ' = *(unsigned char *)$' + m)
    return


_0x6547ea = 0xea + (_0x6547 << 8)


def read_and_execute_pkcool():
    dat = read_memory(_0x401000 + 0x30e0, 305)
    write_pkcool(dat, 0x3C)
    execute_script(_pkcool)
    return


_0x6547ea86 = 0x86 + (_0x6547ea << 8)
execute_and_log_command('show')
rdi = 'rdi'

_0x72433a3c0 = 0xc0 + (_0x72433a3 << 8)
_0x6547ea8670 = 0x70 + (_0x6547ea86 << 8)


def write_pkcool(dat, key):
    with open(_pkcool, "wb") as f:
        for b in dat:
            f.write(bytes([ord(b) ^ key]))

    print("Wrote pkcool:")
    print(open(_pkcool, "r").read())
    return


rip = 'rip'
_0x6547ea867000 = 0x00 + (_0x6547ea8670 << 8)
execute_and_log_command('info b')

def remove_stop_listener(u):
    gdb.events.stop.disconnect(u)
    return


rsp = 'rsp'


def set_reg(reg, n):
    gdb.parse_and_eval("$" + reg + " = " + hex(n))
    return


_0x72433a3c000 = 0x00 + (_0x72433a3c0 << 8)
__0x6547ea867000 = _0x6547ea867000
_0x6547ea867d12 = __0x6547ea867000 + 0xd12
_0x6547ea867fa0 = __0x6547ea867000 + 0xfa0
_0x6547ea867fd0 = _0x6547ea867fa0 + 0x30


def manage_last_breakpoint(e):
    global kflag
    if kflag:
        return
    kflag = True
    bps = gdb.breakpoints()
    if not bps:
        return
    bp = bps[-1]
    if bp.location.startswith("*"):
        o = int(bp.location[1:])
        n = o + 0x30
        bp.delete()
        silent_bp(n)
    kflag = False
    return


rsi = 'rsi'


def remove_first_breakpoint(e):
    bps = gdb.breakpoints()
    if bps:
        bps[0].delete()
    return


def read_register_value(reg):
    return gdb.selected_frame().read_register(reg)


offset = 0
rdx = 'rdx'

# START
print("START from tsgdbinary.py")

register_stop_handler(remove_first_breakpoint)
execute_and_log_command("c")

connect_breakpoint_handler(manage_last_breakpoint)

silent_bp(_0x401000 + 0x3e4)
dat = read_memory(_0x401000 + 0x3080, 71)
write_pkcool(dat, 0xD7)
execute_script(_pkcool)
read_and_execute_pkcool()
silent_bp(_0x401000 + 0x3fe)
redirect_null()
weird_globals_run_py()
for i in range(0, 0x30):
    set_reg(rcx, _0x72433a3c000+i)
    set_rdi_rcx_char(rdi, rcx)
    set_reg(rip, _0x401000 + 0x414)
    set_reg(rsi, int.from_bytes(dat[i+0x10], byteorder='little'))
    execute_history(4)
    set_al(rcx)
    silent_bp(_0x401000 + 0x3fe)

remove_breakpoint_listener(manage_last_breakpoint)

connect_breakpoint_handler(update_breakpoint)
remove_stop_listener(remove_first_breakpoint)

for i in range(0, 6):
    set_reg(rdx, 0x1000)
    set_reg(rsi, _0x401000 + 0x3340 + 0x1000*i)
    set_reg(rdi, _0x6547ea867000)
    set_reg(rip, _0x401000 + 0x4d6)
    silent_bp(_0x401000 + 0x7741)
    execute_history(4)
    set_reg(rax, _0x401000 + 0x5a5)
    silent_bp(_0x401000 + 0x77a5)
    set_reg(rip, __0x6547ea867000+idxs[i])
    set_reg(rcx, _0x72433a3c000+offset)
    set_rsi_rcx_ll(rsi, rcx)
    set_addr_to_rax(rsp)
    execute_history(4)
    bps = gdb.breakpoints()
    for olekj in bps:
        olekj.enabled = False
    silent_bp(_0x401000 + 0x77c1)
    set_reg(rsi, read_register_value(rax))
    set_reg(rdi, 0x89fc76aef8d6a8c3)
    set_reg(rcx, _0x6547ea867fd0+offset)
    execute_history(4)
    set_addr_to_rax(rcx)
    offset += 8

reset_output_streams()
set_reg(rdx, 0x30)
set_reg(rsi, _0x6547ea867fa0)
set_reg(rdi, _0x6547ea867fd0)
set_reg(rip, _0x401000 + 0x8cf)
execute_history(4)
gdb.execute(shell_rm)
gdb.execute('set history save off')
