import re
from z3 import *

# Initialize Z3 variables
a = [Bool(f'a_{i}') for i in range(64)]  # 64 inputs
z3_vars = {}  # A dictionary to store intermediate variables

def parse_verilog_line(line):
    # Match lines of the form "assign _03364_ = ~a_61;"
    notm = re.match(r'.*assign (\w+) = ~(\w+);', line)
    # assign _03419_ = ~a_63;
    if notm:
        var, first = notm.groups()

        first = f'z3_vars["{first}"]'

        expr = f'Not({first})'

        return var, expr

    # Match lines of the form "assign _03364_ = ~a_61;"
    andm = re.match(r'.*assign (\w+) = (\w+) & (\w+);', line)
    # assign _03419_ = ~a_63;
    if andm:
        var, first, second = andm.groups()

        first = f'z3_vars["{first}"]'
        second = f'z3_vars["{second}"]'

        expr = f'And({first}, {second})'

        return var, expr

    wire = re.match(r'.*wire (\w+);', line)
    if wire:
        var = wire.group(1)
        return var, None

    return None, None


# Parse Verilog file and build constraints
constraints = []
with open('circuit.v') as f:
    for line in f:
        var, expr = parse_verilog_line(line)
        if var and not expr:
            z3_vars[var] = Bool(var)
        elif var:
            # Execute the expression in the Z3 context to generate a constraint
            constraints.append(z3_vars[var] == eval(expr))

# Set the output constraint (out = True)
constraints.append(z3_vars['out'] == True)
# constraints.append(z3_vars["d_in_0"] == False)
# constraints.append(z3_vars["d_in_1"] == False)
# constraints.append(z3_vars["d_in_2"] == True)

# Inputs to final call q_out_0, 1, 2 = False, False, True


#constraints.append(z3_vars["clk"] == True)
#constraints.append(z3_vars["reset"] == True)

# Add constraints that the input is ascii
for i in range(0, 64, 8):
    constraints.append(a[i] == False)

# Ensure the input is base64 chars
for i in range(0, 64, 8):
#if False:
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == False, a[i+3] == False, a[i+4] == False, a[i+5] == False, a[i+6] == False, a[i+7] == False)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == False, a[i+3] == False, a[i+4] == False, a[i+5] == False, a[i+6] == False, a[i+7] == True)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == False, a[i+3] == False, a[i+4] == False, a[i+5] == False, a[i+6] == True, a[i+7] == False)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == False, a[i+3] == False, a[i+4] == False, a[i+5] == False, a[i+6] == True, a[i+7] == True)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == False, a[i+3] == False, a[i+4] == False, a[i+5] == True, a[i+6] == False, a[i+7] == False)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == False, a[i+3] == False, a[i+4] == False, a[i+5] == True, a[i+6] == False, a[i+7] == True)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == False, a[i+3] == False, a[i+4] == False, a[i+5] == True, a[i+6] == True, a[i+7] == False)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == False, a[i+3] == False, a[i+4] == False, a[i+5] == True, a[i+6] == True, a[i+7] == True)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == False, a[i+3] == False, a[i+4] == True, a[i+5] == False, a[i+6] == False, a[i+7] == False)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == False, a[i+3] == False, a[i+4] == True, a[i+5] == False, a[i+6] == False, a[i+7] == True)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == False, a[i+3] == False, a[i+4] == True, a[i+5] == False, a[i+6] == True, a[i+7] == False)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == False, a[i+3] == False, a[i+4] == True, a[i+5] == False, a[i+6] == True, a[i+7] == True)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == False, a[i+3] == False, a[i+4] == True, a[i+5] == True, a[i+6] == False, a[i+7] == False)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == False, a[i+3] == False, a[i+4] == True, a[i+5] == True, a[i+6] == False, a[i+7] == True)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == False, a[i+3] == False, a[i+4] == True, a[i+5] == True, a[i+6] == True, a[i+7] == False)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == False, a[i+3] == False, a[i+4] == True, a[i+5] == True, a[i+6] == True, a[i+7] == True)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == False, a[i+3] == True, a[i+4] == False, a[i+5] == False, a[i+6] == False, a[i+7] == False)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == False, a[i+3] == True, a[i+4] == False, a[i+5] == False, a[i+6] == False, a[i+7] == True)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == False, a[i+3] == True, a[i+4] == False, a[i+5] == False, a[i+6] == True, a[i+7] == False)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == False, a[i+3] == True, a[i+4] == False, a[i+5] == False, a[i+6] == True, a[i+7] == True)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == False, a[i+3] == True, a[i+4] == False, a[i+5] == True, a[i+6] == False, a[i+7] == False)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == False, a[i+3] == True, a[i+4] == False, a[i+5] == True, a[i+6] == False, a[i+7] == True)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == False, a[i+3] == True, a[i+4] == False, a[i+5] == True, a[i+6] == True, a[i+7] == False)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == False, a[i+3] == True, a[i+4] == False, a[i+5] == True, a[i+6] == True, a[i+7] == True)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == False, a[i+3] == True, a[i+4] == True, a[i+5] == False, a[i+6] == False, a[i+7] == False)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == False, a[i+3] == True, a[i+4] == True, a[i+5] == False, a[i+6] == False, a[i+7] == True)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == False, a[i+3] == True, a[i+4] == True, a[i+5] == False, a[i+6] == True, a[i+7] == False)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == False, a[i+3] == True, a[i+4] == True, a[i+5] == False, a[i+6] == True, a[i+7] == True)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == False, a[i+3] == True, a[i+4] == True, a[i+5] == True, a[i+6] == False, a[i+7] == False)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == False, a[i+3] == True, a[i+4] == True, a[i+5] == True, a[i+6] == False, a[i+7] == True)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == False, a[i+3] == True, a[i+4] == True, a[i+5] == True, a[i+6] == True, a[i+7] == False)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == False, a[i+3] == True, a[i+4] == True, a[i+5] == True, a[i+6] == True, a[i+7] == True)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == True, a[i+3] == False, a[i+4] == False, a[i+5] == False, a[i+6] == False, a[i+7] == False)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == True, a[i+3] == False, a[i+4] == False, a[i+5] == False, a[i+6] == False, a[i+7] == True)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == True, a[i+3] == False, a[i+4] == False, a[i+5] == False, a[i+6] == True, a[i+7] == False)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == True, a[i+3] == False, a[i+4] == False, a[i+5] == False, a[i+6] == True, a[i+7] == True)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == True, a[i+3] == False, a[i+4] == False, a[i+5] == True, a[i+6] == False, a[i+7] == False)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == True, a[i+3] == False, a[i+4] == False, a[i+5] == True, a[i+6] == False, a[i+7] == True)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == True, a[i+3] == False, a[i+4] == False, a[i+5] == True, a[i+6] == True, a[i+7] == False)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == True, a[i+3] == False, a[i+4] == False, a[i+5] == True, a[i+6] == True, a[i+7] == True)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == True, a[i+3] == False, a[i+4] == True, a[i+5] == False, a[i+6] == False, a[i+7] == False)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == True, a[i+3] == False, a[i+4] == True, a[i+5] == False, a[i+6] == False, a[i+7] == True)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == True, a[i+3] == False, a[i+4] == True, a[i+5] == False, a[i+6] == True, a[i+7] == False)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == True, a[i+3] == False, a[i+4] == True, a[i+5] == True, a[i+6] == False, a[i+7] == False)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == True, a[i+3] == False, a[i+4] == True, a[i+5] == True, a[i+6] == False, a[i+7] == True)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == True, a[i+3] == False, a[i+4] == True, a[i+5] == True, a[i+6] == True, a[i+7] == False)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == True, a[i+3] == True, a[i+4] == True, a[i+5] == False, a[i+6] == True, a[i+7] == False)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == True, a[i+3] == True, a[i+4] == True, a[i+5] == False, a[i+6] == True, a[i+7] == True)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == True, a[i+3] == True, a[i+4] == True, a[i+5] == True, a[i+6] == False, a[i+7] == False)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == True, a[i+3] == True, a[i+4] == True, a[i+5] == True, a[i+6] == False, a[i+7] == True)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == True, a[i+3] == True, a[i+4] == True, a[i+5] == True, a[i+6] == True, a[i+7] == False)))
    constraints.append(Not(And(a[i] == False, a[i+1] == False, a[i+2] == True, a[i+3] == True, a[i+4] == True, a[i+5] == True, a[i+6] == True, a[i+7] == True)))
    constraints.append(Not(And(a[i] == False, a[i+1] == True, a[i+2] == False, a[i+3] == False, a[i+4] == False, a[i+5] == False, a[i+6] == False, a[i+7] == False)))
    constraints.append(Not(And(a[i] == False, a[i+1] == True, a[i+2] == False, a[i+3] == True, a[i+4] == True, a[i+5] == False, a[i+6] == True, a[i+7] == True)))
    constraints.append(Not(And(a[i] == False, a[i+1] == True, a[i+2] == False, a[i+3] == True, a[i+4] == True, a[i+5] == True, a[i+6] == False, a[i+7] == False)))
    constraints.append(Not(And(a[i] == False, a[i+1] == True, a[i+2] == False, a[i+3] == True, a[i+4] == True, a[i+5] == True, a[i+6] == False, a[i+7] == True)))
    constraints.append(Not(And(a[i] == False, a[i+1] == True, a[i+2] == False, a[i+3] == True, a[i+4] == True, a[i+5] == True, a[i+6] == True, a[i+7] == False)))
    constraints.append(Not(And(a[i] == False, a[i+1] == True, a[i+2] == True, a[i+3] == False, a[i+4] == False, a[i+5] == False, a[i+6] == False, a[i+7] == False)))
    constraints.append(Not(And(a[i] == False, a[i+1] == True, a[i+2] == True, a[i+3] == True, a[i+4] == True, a[i+5] == False, a[i+6] == True, a[i+7] == True)))
    constraints.append(Not(And(a[i] == False, a[i+1] == True, a[i+2] == True, a[i+3] == True, a[i+4] == True, a[i+5] == True, a[i+6] == False, a[i+7] == False)))
    constraints.append(Not(And(a[i] == False, a[i+1] == True, a[i+2] == True, a[i+3] == True, a[i+4] == True, a[i+5] == True, a[i+6] == False, a[i+7] == True)))
    constraints.append(Not(And(a[i] == False, a[i+1] == True, a[i+2] == True, a[i+3] == True, a[i+4] == True, a[i+5] == True, a[i+6] == True, a[i+7] == False)))
    constraints.append(Not(And(a[i] == False, a[i+1] == True, a[i+2] == True, a[i+3] == True, a[i+4] == True, a[i+5] == True, a[i+6] == True, a[i+7] == True)))

# Solve with Z3
solver = Solver()
solver.add(constraints)

if solver.check() == sat:
    model = solver.model()
    bits = []
    for i in range(64):
        if model[a[i]]:
            bits.append(1)
        else:
            bits.append(0)
    byte_array = bytearray()
    for i in range(0, 64, 8):
        byte = int(''.join(map(str, bits[i:i+8])), 2)
        byte_array.append(byte)
    print(byte_array.decode('latin-1'))

    print("q_out_0: ", model[z3_vars["q_out_0"]])
    print("q_out_1: ", model[z3_vars["q_out_1"]])
    print("q_out_2: ", model[z3_vars["q_out_2"]])


    solver.add(And(*list(model[a[i]] != a[i] for i in range(64))))

    while solver.check() == sat:
        model = solver.model()
        bits = []
        for i in range(64):
            if model[a[i]]:
                bits.append(1)
            else:
                bits.append(0)
        byte_array = bytearray()
        for i in range(0, 64, 8):
            byte = int(''.join(map(str, bits[i:i+8])), 2)
            byte_array.append(byte)
        print(byte_array.decode('latin-1'))

        print("q_out_0: ", model[z3_vars["q_out_0"]])
        print("q_out_1: ", model[z3_vars["q_out_1"]])
        print("q_out_2: ", model[z3_vars["q_out_2"]])

        solver.add(And(*list(model[a[i]] != a[i] for i in range(64))))
        # solver.add(And(a[i] != int(bool(model[a[i]])) for i in range(64)))
                

else:
    print("No solution found.")