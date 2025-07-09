#!/usr/bin/python
#
# Peteris Krumins (peter@catonmat.net)
# http://www.catonmat.net  --  good coders code, great reuse
#
# Turing Machine simulator for Busy Beaver problem.
# More info at: http://www.catonmat.net/blog/busy-beaver
#
# Version 1.0
#

import sys

class Error(Exception):
    pass

class TuringMachine(object):
    def __init__(self, program, start, halt, init):
        self.program = program
        self.start = start
        self.halt = halt
        self.init = init
        self.tape = [self.init]
        self.pos = 0
        self.state = self.start
        self.set_tape_callback(None)
        self.tape_changed = 1
        self.movez = 0

    def run(self):
        tape_callback = self.get_tape_callback()
        while self.state != self.halt:
            lhs = self.get_lhs()
            rhs = self.get_rhs(lhs)

            if tape_callback:
                tape_callback(self.tape, self.tape_changed, lhs, rhs)
            new_state, new_symbol, move = rhs

            old_symbol = lhs[1]
            self.update_tape(old_symbol, new_symbol)
            self.update_state(new_state)
            self.move_head(move)

        if tape_callback:
            tape_callback(self.tape, self.tape_changed)

    def set_tape_callback(self, fn):
        self.tape_callback = fn

    def get_tape_callback(self):
        return self.tape_callback

    property(get_tape_callback, set_tape_callback)

    @property
    def moves(self):
        return self.movez

    def update_tape(self, old_symbol, new_symbol):
        if old_symbol != new_symbol:
            self.tape[self.pos] = new_symbol
            self.tape_changed += 1
        else:
            self.tape_changed = 0

    def update_state(self, state):
        self.state = state

    def get_lhs(self):
        under_cursor = self.tape[self.pos]
        lhs = self.state + under_cursor
        return lhs

    def get_rhs(self, lhs):
        if lhs not in self.program:
            raise Error('Could not find transition for state "%s".' % lhs)
        return self.program[lhs]

    def move_head(self, move):
        if move == 'l':
            self.pos -= 1
        elif move == 'r':
            self.pos += 1
        else:
            raise Error('Unknown move "%s". It can only be left or right.' % move)

        if self.pos < 0:
            self.tape.insert(0, self.init)
            self.pos = 0
        if self.pos >= len(self.tape):
            self.tape.append(self.init)

        self.movez += 1

beaver_programs = [
    { },

    {'a0': 'h1r' },

    {'a0': 'b1r', 'a1': 'b1l',
     'b0': 'a1l', 'b1': 'h1r'},

    {'a0': 'b1r', 'a1': 'h1r',
     'b0': 'c0r', 'b1': 'b1r',
     'c0': 'c1l', 'c1': 'a1l'},

    {'a0': 'b1r', 'a1': 'b1l',
     'b0': 'a1l', 'b1': 'c0l',
     'c0': 'h1r', 'c1': 'd1l',
     'd0': 'd1r', 'd1': 'a0r'},

#     0   1
# a b1r d0l
# b c1l c1r
# c a1l c0r
# d ??? e0l
# e b0r d1l


    {'a0': 'b1r', 'a1': 'd0l',
     'b0': 'c1l', 'b1': 'c1r',
     'c0': 'a1l', 'c1': 'c0r',
     'd0': 'h1r', 'd1': 'e0l',
     'e0': 'b0r', 'e1': 'd1l'},

    {'a0': 'b1r', 'a1': 'e0l',
     'b0': 'c1l', 'b1': 'a0r',
     'c0': 'd1l', 'c1': 'c0r',
     'd0': 'e1l', 'd1': 'f0l',
     'e0': 'a1l', 'e1': 'c1l',
     'f0': 'e1l', 'f1': 'h1r'}
]

idxs = [6719, 7734, 7175, 7680, 3856, 4676, 9873, 8810, 5422, 10563, 8008, 8910, 1970, 9598, 4289, 7907, 9857, 7016, 9372, 6838, 9949, 10104, 9314, 3774, 8816, 8343, 9386, 8484, 8563, 9665, 10212, 3728, 4045, 4724, 8000, 5197, 2041, 3157, 3770, 2088, 3937, 3151, 10262]
c = 0
def busy_beaver(n):
    out = [0] * len(idxs)
    def tape_callback(tape, tape_changed, lhs=None, rhs=None):
        global c
        print(''.join(tape), lhs, rhs)
        for i, j in enumerate(idxs):
            if j == c:
                out[i] = tape.count('1')
        
        if any(x == 0 for x in out):
            c += 1
        else:
            print(bytes(out))
            sys.exit(0)


    program = beaver_programs[n]

    print("Running Busy Beaver with %d states." % n)
    tm = TuringMachine(program, 'a', 'h', '0')
    tm.set_tape_callback(tape_callback)
    tm.run()
    print ("Busy beaver finished in %d steps." % tm.moves)

def usage():
    print( "Usage: %s [1|2|3|4|5|6]" % sys.argv[0])
    print ("Runs Busy Beaver problem for 1 or 2 or 3 or 4 or 5 or 6 states.")
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv[1:]) < 1:
        usage()

    n = int(sys.argv[1])

    if n < 1 or n > 6:
        usage()

    busy_beaver(n)
