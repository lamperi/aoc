data = open('input.txt').read()

example = """#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5"""

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

def solve(input_data, reg0=0):
    lines = input_data.splitlines()
    ip_fun = int(lines[0].split()[1])
    insts = []
    for line in lines[1:]:
        i, a, b, c = line.split()
        insts.append((i, int(a), int(b), int(c)))

    ip = 0
    reg = [0]*6
    reg[0] = reg0
    while 0 <= ip < len(insts):
        i, a, b, c = insts[ip]
        reg[ip_fun] = ip
        exec_inst(i, reg, insts[ip])
        ip = reg[ip_fun]
        ip += 1
        
    return reg[0]

def compiled(part1):
    reg = [0, 0, 0, 0, 0, 0]
    
    # 17-20
    reg[4] += 2 
    reg[4] = reg[4]*reg[4]
    reg[4] = 19*reg[4]
    reg[4] = reg[4]*11
    
    # 21-24
    reg[2] += 5
    reg[2] = 5*22
    reg[2] += 1
    reg[4] = reg[4] + reg[2]
   
    # 25
    if part1:
        # 26
        pass # go to instruction 1
    else:
        # 27-32
        reg[2] = 27
        reg[2] = reg[2] * 28
        reg[2] = 29 + reg[2]
        reg[2] = 30 * reg[2]
        reg[2] = reg[2] * 14
        reg[2] = reg[2] * 32
        # 33-35
        reg[4] += reg[2]
        reg[0] = 0
        pass # go to instuction 1
            

    # 1
    t = reg[4]
    c = 0
    for a in range(1, t+2):
        x,y = divmod(t, a) 
        if y == 0:
            c += a
    return c

print(compiled(True))
print(compiled(False))
print(solve(data))
