from dec import decrypt_header
import sys

class DecryptVMDisasm:
    # Instruction formats
    FMT_NONE = 0    # No operands
    FMT_IMM16 = 1   # 16-bit immediate value
    FMT_MEM = 2     # Memory address (two bytes)
    
    # Instruction definitions: (mnemonic, format, size)
    INSTRUCTIONS = {
        0x00: ("exit", FMT_NONE, 1),
        0x01: ("push", FMT_IMM16, 3),
        0x02: ("load", FMT_MEM, 3),
        0x03: ("addm", FMT_MEM, 3),
        0x04: ("store", FMT_IMM16, 3),
        0x05: ("loads", FMT_NONE, 1),
        0x06: ("stores", FMT_NONE, 1),
        0x07: ("dup", FMT_NONE, 1),
        0x08: ("pop", FMT_NONE, 1),
        0x09: ("add", FMT_NONE, 1),
        0x0A: ("addi", FMT_IMM16, 3),
        0x0B: ("sub", FMT_NONE, 1),
        0x0C: ("div", FMT_NONE, 1),
        0x0D: ("mul", FMT_NONE, 1),
        0x0E: ("jmp", FMT_MEM, 3),
        0x0F: ("jz", FMT_IMM16, 3),
        0x10: ("jnz", FMT_IMM16, 3),
        0x11: ("eq", FMT_NONE, 1),
        0x12: ("lt", FMT_NONE, 1),
        0x13: ("le", FMT_NONE, 1),
        0x14: ("gt", FMT_NONE, 1),
        0x15: ("ge", FMT_NONE, 1),
        0x16: ("cmp", FMT_IMM16, 3),
        0x17: ("setout", FMT_NONE, 1),
        0x18: ("ret0", FMT_NONE, 1),
        0x19: ("setout", FMT_NONE, 1),
        0x1A: ("xor", FMT_NONE, 1),
        0x1B: ("or", FMT_NONE, 1),
        0x1C: ("and", FMT_NONE, 1),
        0x1D: ("mod", FMT_NONE, 1),
        0x1E: ("shl", FMT_NONE, 1),
        0x1F: ("shr", FMT_NONE, 1),
        0x20: ("rol32", FMT_NONE, 1),
        0x21: ("ror32", FMT_NONE, 1),
        0x22: ("rol16", FMT_NONE, 1),
        0x23: ("ror16", FMT_NONE, 1),
        0x24: ("rol8", FMT_NONE, 1),
        0x25: ("ror8", FMT_NONE, 1),
        0x26: ("putc", FMT_NONE, 1),
    }

    @staticmethod
    def disassemble(bytecode):
        """Disassemble bytecode into readable assembly"""
        offset = 0
        lines = []
        bytecode = bytearray(bytecode)
        
        while offset < len(bytecode):
            # Get current instruction
            opcode = bytecode[offset]
            
            # Check if opcode exists
            if opcode not in DecryptVMDisasm.INSTRUCTIONS:
                lines.append(f"{offset:04x}: db 0x{opcode:02x}  ; invalid opcode")
                offset += 1
                continue
                
            # Get instruction info
            mnemonic, fmt, size = DecryptVMDisasm.INSTRUCTIONS[opcode]
            
            # Format the instruction based on its type
            if fmt == DecryptVMDisasm.FMT_NONE:
                lines.append(f"{offset:04x}: {mnemonic}")
                
            elif fmt == DecryptVMDisasm.FMT_IMM16:
                if offset + 2 >= len(bytecode):
                    lines.append(f"{offset:04x}: {mnemonic} ???  ; truncated")
                    break
                value = bytecode[offset + 2] | (bytecode[offset + 1] << 8)
                lines.append(f"{offset:04x}: {mnemonic} 0x{value:04x}")
                
            elif fmt == DecryptVMDisasm.FMT_MEM:
                if offset + 2 >= len(bytecode):
                    lines.append(f"{offset:04x}: {mnemonic} ???  ; truncated")
                    break
                addr = bytecode[offset + 2] | (bytecode[offset + 1] << 8)
                lines.append(f"{offset:04x}: {mnemonic} [0x{addr:04x}]")
            
            offset += size
            
        return "\n".join(lines)

    @staticmethod
    def disassemble_bytes(bytecode):
        """Disassemble showing both instruction and raw bytes"""
        offset = 0
        lines = []
        bytecode = bytearray(bytecode)
        
        while offset < len(bytecode):
            opcode = bytecode[offset]
            
            if opcode not in DecryptVMDisasm.INSTRUCTIONS:
                raw_bytes = f"{opcode:02x}"
                lines.append(f"{offset:04x}: {raw_bytes:<8} db 0x{opcode:02x}  ; invalid")
                offset += 1
                continue
                
            mnemonic, fmt, size = DecryptVMDisasm.INSTRUCTIONS[opcode]
            
            # Get raw bytes
            if offset + size <= len(bytecode):
                raw_bytes = " ".join(f"{b:02x}" for b in bytecode[offset:offset + size])
            else:
                raw_bytes = " ".join(f"{b:02x}" for b in bytecode[offset:])
                
            # Format instruction
            if fmt == DecryptVMDisasm.FMT_NONE:
                lines.append(f"{offset:04x}: {raw_bytes:<8} {mnemonic}")
                
            elif fmt == DecryptVMDisasm.FMT_IMM16:
                if offset + 2 >= len(bytecode):
                    lines.append(f"{offset:04x}: {raw_bytes:<8} {mnemonic} ???  ; truncated")
                    break
                value = bytecode[offset + 2] | (bytecode[offset + 1] << 8)
                lines.append(f"{offset:04x}: {raw_bytes:<8} {mnemonic} 0x{value:04x}")
                
            elif fmt == DecryptVMDisasm.FMT_MEM:
                if offset + 2 >= len(bytecode):
                    lines.append(f"{offset:04x}: {raw_bytes:<8} {mnemonic} ???  ; truncated")
                    break
                addr = bytecode[offset + 2] | (bytecode[offset + 1] << 8)
                lines.append(f"{offset:04x}: {raw_bytes:<8} {mnemonic} [0x{addr:04x}]")
            
            offset += size
            
        return "\n".join(lines)

class DecryptVM:
    def __init__(self, input_key):
        self.vm = 0  # instruction pointer
        self.input_key = bytearray(input_key)  # Program bytes
        self.stack = []  # Stack for operations
        self.memory = bytearray(2048)  # Memory array (arbitrary size)
        self.decrypt_out = 0  # Output value
        
    def read_uint16(self):
        """Read a 16-bit value from the instruction stream"""
        value = self.input_key[self.vm + 1] | (self.input_key[self.vm] << 8)
        self.vm += 2
        return value

    def get_memory_address(self):
        """Calculate memory address from two bytes"""
        return 256 * self.input_key[self.vm] + self.input_key[self.vm + 1]

    def print_char(self, char):
        """Print a character (simplified from UEFI version)"""
        print(chr(char), end='')

    def execute(self):
        while True:
            if self.vm >= len(self.input_key):
                return 3  # Error: out of bounds
                
            opcode = self.input_key[self.vm]
            self.vm += 1

            # print(f"VM: {self.vm:04X}, Opcode: {opcode:02X}, Stack: {[hex(x) for x in self.stack]}")

            try:
                if opcode == 0x00:  # Exit
                    return 4

                elif opcode == 0x01:  # Push immediate
                    self.stack.append(self.read_uint16())

                elif opcode == 0x02:  # Load from memory array
                    addr = self.get_memory_address()
                    self.vm += 2
                    self.stack.append(self.memory[addr])

                elif opcode == 0x03:  # Add from memory array
                    addr = self.get_memory_address()
                    self.vm += 2
                    self.stack[-1] += self.memory[addr]

                elif opcode == 0x04:  # Store to memory array
                    addr = self.read_uint16()
                    value = self.stack.pop()
                    self.memory[addr] = value & 0xFF

                elif opcode == 0x05:  # Load from stack offset
                    offset = self.stack.pop()
                    self.stack.append(self.memory[offset])

                elif opcode == 0x06:  # Store to stack offset
                    value = self.stack.pop()
                    offset = self.stack.pop()
                    self.memory[offset] = value & 0xFF

                elif opcode == 0x07:  # Push stack value as pointer
                    self.stack.append(self.stack[-1])

                elif opcode == 0x08:  # Pop
                    self.stack.pop()

                elif opcode == 0x09:  # Add top two values
                    value = self.stack.pop()
                    self.stack[-1] += value

                elif opcode == 0x0A:  # Add immediate to stack top
                    self.stack[-1] += self.read_uint16()

                elif opcode == 0x0B:  # Subtract
                    value = self.stack.pop()
                    self.stack[-1] -= value

                elif opcode == 0x0C:  # Division
                    divisor = self.stack.pop()
                    if divisor == 0:
                        return 1
                    self.stack[-1] //= divisor

                elif opcode == 0x0D:  # Multiply
                    value = self.stack.pop()
                    self.stack[-1] *= value

                elif opcode == 0x0E:  # Jump absolute
                    addr = self.get_memory_address()
                    self.vm = addr

                elif opcode == 0x0F:  # Jump if zero
                    target = self.read_uint16()
                    condition = self.stack.pop()
                    if condition:
                        self.vm = target

                elif opcode == 0x10:  # Jump if not zero
                    target = self.read_uint16()
                    condition = self.stack.pop()
                    if not condition:
                        self.vm = target

                elif opcode == 0x11:  # Equal
                    value = self.stack.pop()
                    self.stack[-1] = int(self.stack[-1] == value)

                elif opcode == 0x12:  # Less than
                    value = self.stack.pop()
                    self.stack[-1] = int(self.stack[-1] < value)

                elif opcode == 0x13:  # Less than or equal
                    value = self.stack.pop()
                    self.stack[-1] = int(self.stack[-1] <= value)

                elif opcode == 0x14:  # Greater than
                    value = self.stack.pop()
                    self.stack[-1] = int(self.stack[-1] > value)

                elif opcode == 0x15:  # Greater than or equal
                    value = self.stack.pop()
                    self.stack[-1] = int(self.stack[-1] >= value)

                elif opcode == 0x16:  # Compare with immediate
                    imm = self.read_uint16()
                    self.stack[-1] = int(self.stack[-1] >= imm)

                elif opcode in (0x17, 0x19):  # Set decrypt output
                    self.decrypt_out = self.stack.pop()

                elif opcode == 0x18:  # Return 0
                    return 0

                elif opcode == 0x1A:  # XOR
                    value = self.stack.pop()
                    self.stack[-1] ^= value

                elif opcode == 0x1B:  # OR
                    value = self.stack.pop()
                    self.stack[-1] |= value

                elif opcode == 0x1C:  # AND
                    value = self.stack.pop()
                    self.stack[-1] &= value

                elif opcode == 0x1D:  # Modulo
                    value = self.stack.pop()
                    self.stack[-1] %= value

                elif opcode == 0x1E:  # Left shift
                    value = self.stack.pop()
                    self.stack[-1] <<= value

                elif opcode == 0x1F:  # Right shift
                    value = self.stack.pop()
                    self.stack[-1] >>= value

                elif opcode == 0x20:  # Rotate left 32-bit
                    shift = self.stack.pop() & 0x1F
                    value = self.stack[-1] & 0xFFFFFFFF
                    self.stack[-1] = ((value << shift) | (value >> (32 - shift))) & 0xFFFFFFFF

                elif opcode == 0x21:  # Rotate right 32-bit
                    shift = self.stack.pop() & 0x1F
                    value = self.stack[-1] & 0xFFFFFFFF
                    self.stack[-1] = ((value >> shift) | (value << (32 - shift))) & 0xFFFFFFFF

                elif opcode == 0x22:  # Rotate left 16-bit
                    shift = self.stack.pop() & 0xF
                    value = self.stack[-1] & 0xFFFF
                    self.stack[-1] = ((value << shift) | (value >> (16 - shift))) & 0xFFFF

                elif opcode == 0x23:  # Rotate right 16-bit
                    shift = self.stack.pop() & 0xF
                    value = self.stack[-1] & 0xFFFF
                    self.stack[-1] = ((value >> shift) | (value << (16 - shift))) & 0xFFFF

                elif opcode == 0x24:  # Rotate left 8-bit
                    shift = self.stack.pop() & 0x7
                    value = self.stack[-1] & 0xFF
                    self.stack[-1] = ((value << shift) | (value >> (8 - shift))) & 0xFF

                elif opcode == 0x25:  # Rotate right 8-bit
                    shift = self.stack.pop() & 0x7
                    value = self.stack[-1] & 0xFF
                    self.stack[-1] = ((value >> shift) | (value << (8 - shift))) & 0xFF

                elif opcode == 0x26:  # Print character
                    char = self.stack.pop()
                    self.print_char(char)

                else:
                    return 3  # Unknown opcode

            except (IndexError, ZeroDivisionError) as e:
                print(e)
                return 2  # Stack error


# Example usage:
def decrypt(program_bytes):
    vm = DecryptVM(program_bytes)
    result = vm.execute()
    return result, vm.decrypt_out

def write_input(program_bytes, password):
    vm_offsets = [5, 4, 12, 11, 19, 18, 26, 25, 33, 32, 40, 39, 47, 46, 54, 53]
    for i, offset in enumerate(vm_offsets):
        program_bytes[offset] = password[i]
    return program_bytes



# Test program
if __name__ == "__main__":
    # Example program that prints "Hello!"
    program = [
        0x01, 0, 0x48,  # Push 'H'
        0x26,              # Print it
        0x01, 0, 0x65,  # Push 'e'
        0x26,              # Print it
        0x01, 0, 0x6C,  # Push 'l'
        0x26,              # Print it
        0x01, 0, 0x6C,  # Push 'l'
        0x26,              # Print it
        0x01, 0, 0x6F,  # Push 'o'
        0x26,              # Print it
        0x01, 0, 0x21,  # Push '!'
        0x26,              # Print it
        0x19               # Return 0
    ]

    fname = sys.argv[1]
    data = open(fname, 'rb').read()
    header = decrypt_header(data[:0x10])
    enc = data[0x10:0x10+header.enc_size]
    vm = data[header.vm_offset:header.vm_offset+header.vm_length]

    # disas = DecryptVMDisasm.disassemble_bytes(vm)
    # print(disas)
    # open('vm_disasm.txt', 'w').write(disas)

    vm = bytearray(vm)
    password = b'BrainNumbFromVm!'
    vm = write_input(vm, password)

    result, output = decrypt(vm)
    print(f"\nProgram returned: {result}")
    print(f"Decrypt output: {output}")