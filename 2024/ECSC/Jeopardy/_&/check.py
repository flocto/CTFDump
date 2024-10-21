#!/usr/bin/env python3.12

import subprocess
import sys
from tempfile import NamedTemporaryFile
import re

if len(sys.argv) < 2:
	print('Usage: check.py <flag>')


circuit_v = sys.argv[2] if len(sys.argv) > 2 else 'circuit.v'

if not (match := re.match(r'ECSC{([A-Za-z0-9_\+/]{32})}', sys.argv[1])):
	exit(1)

token = match.group(1).encode()

tb_v = f"""`timescale 1 ns / 1 ns

module main;
  reg [63:0] x;
  wire out;
  reg clk, reset;

  circuit dut (
    .clk(clk), .reset(reset), .out(out),
	.a_0(x[0]), .a_1(x[1]), .a_2(x[2]), .a_3(x[3]), .a_4(x[4]), .a_5(x[5]), .a_6(x[6]), .a_7(x[7]),
    .a_8(x[8]), .a_9(x[9]), .a_10(x[10]), .a_11(x[11]), .a_12(x[12]), .a_13(x[13]), .a_14(x[14]), .a_15(x[15]),
    .a_16(x[16]), .a_17(x[17]), .a_18(x[18]), .a_19(x[19]), .a_20(x[20]), .a_21(x[21]), .a_22(x[22]), .a_23(x[23]),
    .a_24(x[24]), .a_25(x[25]), .a_26(x[26]), .a_27(x[27]), .a_28(x[28]), .a_29(x[29]), .a_30(x[30]), .a_31(x[31]),
	.a_32(x[32]), .a_33(x[33]), .a_34(x[34]), .a_35(x[35]), .a_36(x[36]), .a_37(x[37]), .a_38(x[38]), .a_39(x[39]),
	.a_40(x[40]), .a_41(x[41]), .a_42(x[42]), .a_43(x[43]), .a_44(x[44]), .a_45(x[45]), .a_46(x[46]), .a_47(x[47]),
	.a_48(x[48]), .a_49(x[49]), .a_50(x[50]), .a_51(x[51]), .a_52(x[52]), .a_53(x[53]), .a_54(x[54]), .a_55(x[55]),
	.a_56(x[56]), .a_57(x[57]), .a_58(x[58]), .a_59(x[59]), .a_60(x[60]), .a_61(x[61]), .a_62(x[62]), .a_63(x[63])
  );

  initial
    clk = 1'b0;

  always
    #25 clk = ~clk;
  
  initial begin
    reset = 1'b1;
    #10
    reset = 1'b0;

	{'\n'.join(f"""x = {{8'h{token[i]:02X}, 8'h{token[i+1]:02X}, 8'h{token[i+2]:02X}, 8'h{token[i+3]:02X}, 8'h{token[i+4]:02X}, 8'h{token[i+5]:02X}, 8'h{token[i+6]:02X}, 8'h{token[i+7]:02X}}};\n#50""" for i in range(0, len(token), 8))}

    #10
    $display("Output = %h", out);
    $finish;
  end
endmodule
"""

with NamedTemporaryFile('w', suffix='.v', delete_on_close=False) as tb, NamedTemporaryFile('w', delete_on_close=False) as out:
	tb.write(tb_v)
	tb.close()

	out.close()

	subprocess.check_call(['iverilog', circuit_v, tb.name, '-o', out.name])
	res = subprocess.check_output(['vvp', out.name])

print(res.decode(), end='')