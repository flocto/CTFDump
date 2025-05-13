#!/usr/bin/env python3
import random
import PIL.Image
import numpy as np
from PIL import Image
import pickle
import secrets
from m import Memory
from r import Registers
from t import T
from f import Flags


def finish():
    flags.clear(0)
    exit("congrats, you can get flag")


def flag_set():
    flags.set_bit(1, tb.compute_check[regs.get(0), regs.get(1)])
    flags.set_bit(13, tb.reg_check[regs.get(0), regs.get(1)])
    flags.set_bit(14, tb.flag_check[regs.get(0), regs.get(1)])


comp_passed = 0
def compute(instr):
    global comp_passed
    if flags.get_bit(2):
        return
    cur_h = hash((tuple(regs.get_hash()), flags.get_hash(),
                 tuple(memory.get_hash().tolist())))
    # print(f"compute = {cur_h} -> {tb.compute_hash[regs.get(0), regs.get(1)]}")
    # print((tuple(regs.get_hash()), flags.get_hash(),
    #              tuple(me.get_hash().tolist())))
    if cur_h == tb.compute_hash[regs.get(0), regs.get(1)]:
        comp_passed += 1
        memory.s()
        try:
            instr = instr[regs.get(1)+1:]
        except IndexError:
            flags.set_bit(2)
            regs.set(10, 69)
        regs.set(tb.reg_scrable[regs.get(0)][0],
                 tb.reg_scrable[regs.get(0)][1])
        regs.set(0, 1+regs.get(0))
        regs.set(1, 0)
    else:
        flags.set_bit(2)
    return instr


flag_passed = 0
def flag_check():
    global flag_passed
    # print(f"flag_check({flags.get_num()}) -> {tb.flag_hash[regs.get(0), regs.get(1)]}")
    cur_num = flags.get_num()
    if cur_num != tb.flag_hash[regs.get(0), regs.get(1)]:
        flags.set_bit(2)
    else:
        flag_passed += 1


reg_passed = 0
def reg_check():
    global reg_passed
    # print(f"reg_check({regs.get_hash()}) -> {tb.reg_hash[regs.get(0), regs.get(1)]}")
    cur_h = regs.get_hash()
    if cur_h != tb.reg_hash[regs.get(0), regs.get(1)].tolist():
        flags.set_bit(2)
    else:
        reg_passed += 1


def err_check():
    if regs.get(10):
        flags.set_bit(2)


def start():
    if regs.get(0)+regs.get(1) != 0:
        flags.set_bit(2)
    else:
        flags.set_bit(0)
        flags.set_bit(1)


def rt():
    flags.clear(3)
    flags.toggle(4)
    flags.clear(5)
    flags.clear(6)
    flags.clear(7)
    flags.clear(8)
    flags.clear(9)
    flags.clear(10)
    flags.clear(11)
    flags.clear(12)
    flags.clear(13)
    flags.clear(14)
    flags.clear(15)
    regs.set(6, 0)
    regs.set(7, 0)
    regs.set(8, 0)
    regs.set(9, 0)
    regs.set(10, 0)


def greater_than():
    try:
        if regs.get(regs.get(3)) < regs.get(regs.get(4)):
            flags.set_bit(12)
    except IndexError:
        flags.set_bit(2)


def load_imm(ins):
    # print(f"load_imm({ord(ins)})")
    regs.set(5, ord(ins))
    flags.set_bit(3)
    flags.toggle(5)


def c_i():
    flags.set_bit(1)
    flags.toggle(6)


def incr(ins):
    regs.set(ord(ins)-9, 1+regs.get(ord(ins)-9))
    flags.toggle(7)


def mov_reg(src, dst):
    regs.set(dst, regs.get(src))
    flags.toggle(11)


def andd(ins):
    try:
        regs.set(regs.get(5), regs.get(regs.get(4)) & regs.get(ord(ins)-0x20))
    except IndexError:
        flags.set_bit(2)


def xor(ins):
    try:
        regs.set(ord(ins)-0x28, regs.get(regs.get(3)) ^ regs.get(regs.get(4)))
    except IndexError:
        flags.set_bit(2)


def flags_to_reg(ins):
    regs.set(ord(ins)-0x30, flags.get_num())
    flags.toggle(10)


def add(ins):
    try:
        regs.set(ord(ins)-0x38, regs.get(regs.get(3))+regs.get(regs.get(4)))
    except IndexError:
        flags.set_bit(2)
    flags.toggle(8)


def load_mask(ins):
    memory.mask(tb.masks[ord(ins)-0x01], 37*regs.get(2)+regs.get(1))
    flags.toggle(15)

flags = Flags()
memory = Memory()
tb = T()
regs = Registers()
def main(insts, print=lambda *x: None):
    insts = insts.decode("latin-1")
    global flags, memory, tb, regs
    flags = Flags()
    memory = Memory()
    tb = T()
    regs = Registers()
    last = regs.get_hash()[:2]
    while True:
        if flags.get_bit(2):
            # exit()
            return
        if regs.get(0) == 11:
            finish()
        flag_set()
        try:
            inst = insts[regs.get(1)]
        except IndexError:
            flags.set_bit(2)

        if regs.get_hash()[:2] == last:
            flags.set_bit(2) # infinite loop

        print(f"regs: {regs.get_hash()}")
        # print(f"flags: {flags}")
        # print(f"me: {me.get_buf()}")
        print(f"ins: {ord(inst)}")

        if inst == "\x00" and not flags.get_bit(2):
            start()
        elif flags.get_bit(3) and flags.get_bit(0) and not flags.get_bit(2):
            regs.set(regs.get(5), ord(inst))
            flags.clear(3)
        elif flags.get_bit(0) and not flags.get_bit(2):
            match inst:
                case "\x01":
                    rt()
                case "\x02":
                    greater_than()
                case inst if ord(inst) < 11:
                    load_imm(inst)
                case inst if ord(inst) < 0x13:
                    incr(inst)
                case "\x13": # reg[8] = reg[0]
                    mov_reg(0, 8)
                case "\x14": # reg[4] = reg[0]
                    mov_reg(0, 4)
                case "\x15": # reg[4] = reg[3]
                    mov_reg(3, 4) 
                case "\x16": # reg[2] = reg[4]
                    mov_reg(4, 2)
                case "\x17": # reg[5] = reg[4]
                    mov_reg(4, 5)
                case "\x18": # reg[7] = reg[5]
                    mov_reg(5, 7)
                case "\x19": # reg[4] = reg[6]
                    mov_reg(6, 4)
                case "\x1a":
                    mov_reg(8, 5)
                case "\x1b":
                    mov_reg(8, 10)
                case "\x1c":
                    mov_reg(7, 2)
                case "\x1d":
                    mov_reg(7, 10)
                case "\x1e":
                    mov_reg(9, 3)
                case "\x1f":
                    mov_reg(10, 8)
                case inst if ord(inst) < 0x2a: # reg[5] = reg[4] & ord(inst) - 0x20
                    andd(inst)
                case inst if ord(inst) < 0x32:
                    xor(inst)
                case inst if ord(inst) < 0x3a:
                    flags_to_reg(inst)
                case inst if ord(inst) < 0x42:
                    add(inst)
                case inst if ord(inst) < 253:
                    load_mask(inst)
                case "\xff":
                    c_i()
                case _:
                    flags.set_bit(2)
        else:
            print("EXITED FROM VM")
            return 1
        err_check()
        if flags.get_bit(13):
            print(f"reg_check @ {regs.get(0)} {regs.get(1)}") 
            reg_check()
        if flags.get_bit(14):
            print(f"flag_check @ {regs.get(0)} {regs.get(1)}")
            flag_check()
        err_check()
        if flags.get_bit(1):
            print(f"compute_check @ {regs.get(0)} {regs.get(1)}")
            insts = compute(insts)
        else:
            regs.set(1, 1+regs.get(1))
        err_check()

if __name__ == "__main__":
    insts = input("What's up ('til newline ofc)? ")
    main(insts)
    