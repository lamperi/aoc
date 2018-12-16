import re
data = open('input.txt').read()

def check_opcode(reg, code, after):
    valids = []
    _, a, b, c = code
    if reg[a] + reg[b] == after[c]:
        valids.append('addr')
    if reg[a] + b == after[c]:
        valids.append('addi')
    if reg[a] * reg[b] == after[c]:
        valids.append('mulr')
    if reg[a] * b == after[c]:
        valids.append('muli')
    if reg[a] & reg[b] == after[c]:
        valids.append('banr')
    if reg[a] & b == after[c]:
        valids.append('bani')
    if reg[a] | reg[b] == after[c]:
        valids.append('borr')
    if reg[a] | b == after[c]:
        valids.append('bori')
    if reg[a] == after[c]:
        valids.append('setr')
    if a == after[c]:
        valids.append('seti')
    if after[c] == 1 and a > reg[b]:
        valids.append('gtir')
    if after[c] == 0 and a <= reg[b]:
        valids.append('gtir')
    if after[c] == 1 and reg[a] > b:
        valids.append('gtri')
    if after[c] == 0 and reg[a] <= b:
        valids.append('gtri')
    if after[c] == 1 and reg[a] > reg[b]:
        valids.append('gtrr')
    if after[c] == 0 and reg[a] <= reg[b]:
        valids.append('gtrr')
    if after[c] == 1 and a == reg[b]:
        valids.append('eqir')
    if after[c] == 0 and a != reg[b]:
        valids.append('eqir')
    if after[c] == 1 and reg[a] == b:
        valids.append('eqri')
    if after[c] == 0 and reg[a] != b:
        valids.append('eqri')
    if after[c] == 1 and reg[a] == reg[b]:
        valids.append('eqrr')
    if after[c] == 0 and reg[a] != reg[b]:
        valids.append('eqrr')
    return valids


def exec_inst(mapping, reg, code):
    inst, a, b, c = code
    inst_name = mapping[inst]
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


def solve(data):
    next_inst = False
    cases = []
    program = []
    for line in data.splitlines():
        if "Before" in line:
            bef_state = list(map(int, re.findall(r'-?\d+', line)))
            next_inst = True
        elif next_inst:
            inst = list(map(int, re.findall(r'-?\d+', line)))
            next_inst = False
        elif "After" in line:
            after_state = list(map(int, re.findall(r'-?\d+', line)))
            cases.append((bef_state, inst, after_state))
        else:
            inst = list(map(int, re.findall(r'-?\d+', line)))
            if len(inst) == 4:
                program.append(inst)

    s = 0
    for case in cases:
        if len(check_opcode(*case)) >= 3:
            s += 1

    op_code = {}
    for case in cases:
        valids = check_opcode(*case)
        inst = case[1][0]
        if inst not in op_code:
            op_code[inst] = set(valids)
        else:
            op_code[inst] = op_code[inst].intersection(set(valids))
    
    mapping = {}
    while len(mapping) < 16:
        for inst, valids in op_code.items():
            if len(valids) == 1:
                mapping[inst] = list(valids)[0]
        for inst, valids in op_code.items():
            op_code[inst] = valids - set(mapping.values())

    assert len(mapping) == 16
    assert len(set(mapping.values())) == 16

    reg = [0, 0, 0, 0]
    for code in program:
        exec_inst(mapping, reg, code)
    return s, reg[0]


print(check_opcode([3, 2, 1, 1], [9, 2, 1, 2], [3, 2, 2, 1]))
print(solve(data))