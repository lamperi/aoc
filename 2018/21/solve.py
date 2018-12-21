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

def solve(input_data):
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
    
    return '{}\n{}'.format(first_halting, last_halting_before_loop)

def compiled():
    # TODO
    r0, r1, r2, r3, r4, r5 = 0, 0, 0, 0, 0, 0

print(solve(data))
