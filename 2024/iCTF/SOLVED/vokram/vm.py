#!/usr/bin/env python3
def vokram(text: str, program):
    while True:
        for pat, repl, stop in program:
            if pat in text:
                text = text.replace(pat, repl, 1)
                if stop:
                    return text
                break
        else:
            return text
        
def vokram_test(text: str, program):
    c = 0
    while True:
        if len(text) > 300:
            print('FAILED')
            print(text)
            break
        for pat, repl, stop in program:
            if pat in text:
                if '|' in pat:
                    # print(text)
                    print(text.split('|')[-1][1:])
                    # input(f'{c}')
                    c += 1
                    if c == 15:
                        return text.split('|')[-1][1:]
                text = text.replace(pat, repl, 1)
                # if '😢' in repl:
                #     print(text)
                #     input()
                if stop:
                    return text
                break
        else:
            return text



def parse(source):
    program = []
    for line in source.strip().splitlines():
        pat, repl = line.split(":", 1)
        stop = False
        if len(repl) > 0 and repl[0] == ":":
            repl = repl[1:]
            stop = True
        if ":" in repl:
            raise ValueError("invalid rule: %r" % line)
        program.append((pat, repl, stop))
    return program


if __name__ == "__main__":
    import sys

    source_file = sys.argv[1]
    input_str = sys.argv[2]
    with open(source_file) as f:
        program = parse(f.read())

    print(program)
    print(vokram(input_str, program))
