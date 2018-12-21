data = open('input.txt').read()

def exec_inst(inst_name, reg, code):
    _, a, b, c = code
    if inst_name == 'addr':
        reg[c] = reg[a] + reg[b]
    elif inst_name == 'addi':
        reg[c] = reg[a] + b
    elif inst_name == 'mulr':
        reg[c] = reg[a] * reg[b]
    elif inst_name == 'muli':
        reg[c] = reg[a] * b
    elif inst_name == 'banr':
        reg[c] = reg[a] & reg[b]
    elif inst_name == 'bani':
        reg[c] = reg[a] & b
    elif inst_name == 'borr':
        reg[c] = reg[a] | reg[b]
    elif inst_name == 'bori':
        reg[c] = reg[a] | b
    elif inst_name == 'setr':
        reg[c] = reg[a]
    elif inst_name == 'seti':
        reg[c] = a
    elif inst_name == 'gtir':
        reg[c] = 1 if a > reg[b] else 0
    elif inst_name == 'gtri':
        reg[c] = 1 if reg[a] > b else 0
    elif inst_name == 'gtrr':
        reg[c] = 1 if reg[a] > reg[b] else 0
    elif inst_name == 'eqir':
        reg[c] = 1 if a == reg[b] else 0
    elif inst_name == 'eqri':
        reg[c] = 1 if reg[a] == b else 0
    elif inst_name == 'eqrr':
        reg[c] = 1 if reg[a] == reg[b] else 0
    else:
        assert False

def solve(input_data, part1):
    lines = input_data.splitlines()
    ip_fun = int(lines[0].split()[1])
    insts = []
    for line in lines[1:]:
        i, a, b, c = line.split()
        insts.append((i, int(a), int(b), int(c)))

    ip = 0
    reg = [0]*6
    seen = set()
    first_halting = None
    last_halting_before_loop = None
    while 0 <= ip < len(insts):
        if ip == 28:
            r3 = reg[3]
            if first_halting is None:
                first_halting = r3
                if part1:
                    break
            if r3 not in seen:
                seen.add(r3)
            else:
                break
            last_halting_before_loop = r3
        if ip == 18: # Optimize inner loop
            r2 = reg[2]
            r5 = reg[5]
            while 256*(r2+1) <= r5:
                r2 += 1
            reg[2] = r2
            reg[5] = r5
            ip = 26
        else:
            i, a, b, c = insts[ip]
            reg[ip_fun] = ip
            exec_inst(i, reg, insts[ip])
            ip = reg[ip_fun]
            ip += 1
    
    if part1:
        return first_halting
    else:
        return last_halting_before_loop

def compiled(part1):
    seen = set()
    last_halting_before_loop = None

    r0, r1, r2, r3, r4, r5 = 0, 0, 0, 0, 0, 0
    r3 = 123
    r3 = r3 & 456
    r3 = 1 if r3 == 72 else 0
    assert r3 != 0
    r3 = 0
    while True:
        r5 = r3 | 65536 # Line 06
        r3 = 15028787
        while True:
            r2 = r5 & 255 # Line 08
            r3 = r3 + r2
            r3 = r3 & 16777215
            r3 = r3 * 65899
            r3 = r3 & 16777215
            r2 = 1 if 256 > r5 else 0
            if r2: # Lines 14 & 16
                if r0 == r3: # Line 28
                    return # Line 29
                else:
                    ### Start custom code to solve this
                    if part1:
                        return r3
                    else:
                        if r3 in seen:
                            return last_halting_before_loop
                        seen.add(r3)
                        last_halting_before_loop = r3
                    ### End custom code to solve this
                    break # Goto line 06
            else:
                pass # Line 15

            r2 = 0 # Line 17
            while True:
                r4 = r2 + 1 # Line 18
                r4 = r4 * 256
                r4 = 1 if r4 > r5 else 0
                if r4: # Line 21 and 23
                    r5 = r2 # Line 26
                    break # Goto 08
                r2 = r2 + 1
                continue # Goto 18

if __name__ == "__main__":
    import sys, functools
    solver = compiled
    if len(sys.argv) > 1:
        if 'slow' in sys.argv:
            solver = functools.partial(solve, data)
        parts = []
        if '1' in sys.argv:
            parts.append((True, 13270004))
        if '2' in sys.argv:
            parts.append((False, 12879142))
        for part, result in (parts or [(True, 13270004)]):
            assert solver(part) == result
    else:
        print('Part 1 slow: ', solve(data, True))
        print('Part 1 fast: ', compiled(True))
        print('Part 2 slow: ', solve(data, False))
        print('Part 2 fast: ', compiled(False))
