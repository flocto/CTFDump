def parse(vm):
    ip = 0

    while ip < len(vm):
        opcode = vm[ip]

        match opcode:
            case 0:
                reg_id, c = vm[ip + 1:ip + 3]
                ip += 3
                print(f"reg[{reg_id}] = {c}")
            case 1:
                a, b = vm[ip + 1:ip + 3]
                ip += 3
                print(f"reg[{a}] ^= reg[{b}]")
            case 2:
                a, b = vm[ip + 1:ip + 3]
                ip += 3
                print(f"reg[{a}] = rotl(reg[{a}], {b})")
            case 3:
                a = vm[ip + 1]
                ip += 2
                print(f"reg[{a}] = sbox[reg[{a}]]")
            case 4:
                a, b = vm[ip + 1:ip + 3]
                ip += 3
                print(f"mem[{b}] = reg[{a}]")
            case 5:
                a, b = vm[ip + 1:ip + 3]
                ip += 3
                print(f"reg[{a}] = mem[{b}]")
            case 6:
                a = vm[ip + 1]
                ip += 2
                print(f"putc {a}")
            case 7:
                print("halt")
                break
            case 8:
                a, b = vm[ip + 1:ip + 3]
                ip += 3
                print(f"reg[{a}] = rotr(reg[{a}], {b})")
        

def gen_vm(msg:bytes):
    vm = []
    init = [0xaa, 0xbb, 0xcc, 0xdd, 0xee]

    for i, c in enumerate(msg):
        vm.extend([0, 1, c])
    
        for j in range(10):
            vm.extend([0, 0, init[(i * 10 + j) % 5]])
            vm.extend([8, 1, 3])
            vm.extend([3, 1])
            vm.extend([1, 1, 0])
            vm.extend([2, 1, 3])
        
        vm.extend([4, 1, i])
    
    vm.append(7)

    return vm

vm = gen_vm(b'csawctf{')
parse(vm)