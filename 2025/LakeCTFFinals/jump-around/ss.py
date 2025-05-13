# skibidi_loop_fast4.py
import re

import gdb

BASE_ADDR = 0x555555554000
OFFSET = 0xb208
TARGET_ADDR = BASE_ADDR + OFFSET
OUTPUT_FILE = "skibidi"

# add any function-entry addresses here to skip stepping into
SKIP_TARGETS = {0x5555555551a0}


class SkibidiLoopFast4(gdb.Command):
    """Silent dump, no duplicates, indent by real-call depth,
       skip stubs + PLT + SKIP_TARGETS, print regs on calls."""

    def __init__(self):
        super().__init__("skibidi_loop", gdb.COMMAND_USER)
        self.plt_start = None
        self.plt_end = None
        self.skip_next_call = False
        self.dumped = set()
        self.call_depth = 0
        self.max_depth = 0
        self.out = None

    def find_plt_range(self):
        info = gdb.execute("info files", to_string=True)
        for line in info.splitlines():
            m = re.search(
                r'0x([0-9a-f]+)\s*-\s*0x([0-9a-f]+)\s+is\s+\.plt', line)
            if m:
                self.plt_start = int(m.group(1), 16)
                self.plt_end = int(m.group(2), 16)
                return
        # no .plt found → won't treat any call as plt

    def disas(self, addr):
        return gdb.execute(f"x/1i {addr}", to_string=True).strip()

    def extract_call_target(self, disas):
        m = re.search(r'\bcallq?\s+(0x[0-9a-f]+)', disas)
        return int(m.group(1), 16) if m else None

    def is_plt_call(self, disas):
        return "plt" in disas

    def is_skip_target(self, disas):
        tgt = self.extract_call_target(disas)
        return tgt in SKIP_TARGETS

    def fetch_regs(self):
        # fetch as ints, then format
        regs = {
            'rdi': int(gdb.parse_and_eval("$rdi")),
            'rsi': int(gdb.parse_and_eval("$rsi")),
            'rdx': int(gdb.parse_and_eval("$rdx")),
            'rcx': int(gdb.parse_and_eval("$rcx")),
        }
        return " ".join(f"{k}=0x{v:x}" for k, v in regs.items())

    def invoke(self, arg, from_tty):
        gdb.execute("set pagination off", to_string=True)
        gdb.execute("set disassembly-flavor intel", to_string=True)

        self.out = open(OUTPUT_FILE, "w")
        self.find_plt_range()

        gdb.Breakpoint(f"*0x{TARGET_ADDR:x}")
        gdb.execute("run", to_string=True)

        while True:
            try:
                pc = int(gdb.parse_and_eval("$pc"))
                disas = self.disas(pc)

                # unwind depth on returns
                if re.match(r'\s*retq?\b', disas) and self.call_depth:
                    self.call_depth -= 1

                # stub skips
                skip = False
                if re.search(r'\blea\s+rsp,\s*\[rsp\+0x2008\]', disas):
                    skip = True
                    self.skip_next_call = False
                elif re.search(r'\blea\s+rsp,\s*\[rsp-0x2000\]', disas):
                    skip = True
                    self.skip_next_call = True
                elif self.skip_next_call and re.search(r'\bcallq?\b', disas):
                    skip = True
                    self.skip_next_call = False

                # dump if new & not stub-skipped
                was_call = False
                if not skip and pc not in self.dumped:
                    indent = "    " * self.call_depth
                    line = indent + disas

                    # for calls, append regs
                    if re.search(r'\bcallq?\b', disas):
                        regs = self.fetch_regs()
                        line += "    [" + regs + "]"

                    self.out.write(line + "\n")
                    self.dumped.add(pc)

                    # will we step into this call?
                    if (re.search(r'\bcallq?\b', disas)
                        and not self.is_plt_call(disas)
                            and not self.is_skip_target(disas)):
                        was_call = True

                # advance: nexti over PLT or skip-target, else stepi
                if self.is_plt_call(disas) or self.is_skip_target(disas) or self.call_depth > self.max_depth:
                    gdb.execute("nexti", to_string=True)
                else:
                    gdb.execute("stepi", to_string=True)

                # only bump depth when we actually stepped in
                if was_call:
                    self.call_depth += 1

                if "ret" in disas:
                    self.call_depth -= 1

            except (gdb.error, KeyboardInterrupt):
                break

        self.out.close()


SkibidiLoopFast4()