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
    #   assign out = q_out_2 & _03430_;
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
            #print(var, expr)
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

    print("d_in_0: ", model[z3_vars["d_in_0"]])
    print("d_in_1: ", model[z3_vars["d_in_1"]])
    print("d_in_2: ", model[z3_vars["d_in_2"]])
    print()

    # Add non-repeating constraint
    #solver.add(Not(And(z3_vars["q_out_0"] == model[z3_vars["q_out_0"]], z3_vars["q_out_1"] == model[z3_vars["q_out_1"]], z3_vars["q_out_2"] == model[z3_vars["q_out_2"]])))

    solver.add(Not(And([a[0] == model[a[0]], a[1] == model[a[1]], a[2] == model[a[2]], a[3] == model[a[3]], a[4] == model[a[4]], a[5] == model[a[5]], a[6] == model[a[6]], a[7] == model[a[7]]])))
    solver.add(Not(And([a[8] == model[a[8]], a[9] == model[a[9]], a[10] == model[a[10]], a[11] == model[a[11]], a[12] == model[a[12]], a[13] == model[a[13]], a[14] == model[a[14]], a[15] == model[a[15]]])))
    solver.add(Not(And([a[16] == model[a[16]], a[17] == model[a[17]], a[18] == model[a[18]], a[19] == model[a[19]], a[20] == model[a[20]], a[21] == model[a[21]], a[22] == model[a[22]], a[23] == model[a[23]]])))
    solver.add(Not(And([a[24] == model[a[24]], a[25] == model[a[25]], a[26] == model[a[26]], a[27] == model[a[27]], a[28] == model[a[28]], a[29] == model[a[29]], a[30] == model[a[30]], a[31] == model[a[31]]])))
    solver.add(Not(And([a[32] == model[a[32]], a[33] == model[a[33]], a[34] == model[a[34]], a[35] == model[a[35]], a[36] == model[a[36]], a[37] == model[a[37]], a[38] == model[a[38]], a[39] == model[a[39]]])))
    solver.add(Not(And([a[40] == model[a[40]], a[41] == model[a[41]], a[42] == model[a[42]], a[43] == model[a[43]], a[44] == model[a[44]], a[45] == model[a[45]], a[46] == model[a[46]], a[47] == model[a[47]]])))
    solver.add(Not(And([a[48] == model[a[48]], a[49] == model[a[49]], a[50] == model[a[50]], a[51] == model[a[51]], a[52] == model[a[52]], a[53] == model[a[53]], a[54] == model[a[54]], a[55] == model[a[55]]])))
    solver.add(Not(And([a[56] == model[a[56]], a[57] == model[a[57]], a[58] == model[a[58]], a[59] == model[a[59]], a[60] == model[a[60]], a[61] == model[a[61]], a[62] == model[a[62]], a[63] == model[a[63]]])))

else:
    print("No solution found.")