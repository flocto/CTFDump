from x64dbg import *

def Log(txt):
    print("[DEBUG] " + txt)

# set stack to A, B, C, D
rsp = Register.GetRSP()
Memory.WriteDword(rsp, 0x41)
Memory.WriteDword(rsp + 8, 0x42)
Memory.WriteDword(rsp + 16, 0x43)
Memory.WriteDword(rsp + 24, 0x44)

# set registers
Register.SetCAX(0x100)
Register.SetCBX(0x200)
Register.SetCCX(0x300)
Register.SetCDX(0x400)
Register.SetCSI(0x500)
Register.SetCDI(0x600)
Register.SetCBP(0x700)
# Register.SetCSP(0x800)
Register.SetR8(0x800)
Register.SetR9(0x900)
Register.SetR10(0xa00)
Register.SetR11(0xb00)
Register.SetR12(0xc00)
Register.SetR13(0xd00)
Register.SetR14(0xe00)
Register.SetR15(0xf00)

Gui.Refresh()