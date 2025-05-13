def main():
    with open('program.bpf', 'r') as f:
        instructions = [int(line.strip()) for line in f.readlines() if line.strip()]
    
    with open('dumped.bin', 'wb') as f:
        for inst in instructions[:20]:
            if inst & 0xff in [0x02, 0x5d]:
                continue
            f.write(inst.to_bytes(8, byteorder='little'))

if __name__ == "__main__":
    main()