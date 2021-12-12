example1 = """set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2"""

example2 = """snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d"""

import os.path
INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read().strip()

# Part 1

def val(var, reg):
    try:
        return int(var)
    except:
        return reg.get(var, 0)


def func1(data):
    insts = []
    for line in data.splitlines():
        parts = line.split()
        insts.append(parts)

    reg = {}
    snd_reg = 0
    ptr = 0
    while 0 <= ptr < len(insts):
        inst = insts[ptr]
        #print(reg, snd_reg, ptr, inst[0])
        if inst[0] == "snd":
            snd_reg = reg.get(inst[1], 0)
        elif inst[0] == "set":
            reg[inst[1]] = val(inst[2], reg)
        elif inst[0] == "add":
            reg[inst[1]] = reg.get(inst[1], 0) + val(inst[2], reg)
        elif inst[0] == "mul":
            reg[inst[1]] = reg.get(inst[1], 0) * val(inst[2], reg)
        elif inst[0] == "mod":
            reg[inst[1]] = reg.get(inst[1], 0) % val(inst[2], reg)
        elif inst[0] == "rcv":
            if val(inst[1], reg) != 0:
                return snd_reg
        elif inst[0] == "jgz":
            if val(inst[1], reg) > 0:
                ptr += val(inst[2], reg)
                continue
        ptr += 1


print(func1(example1))
print(func1(data))

# Part 2


def execute(insts, reg, send, recv, ptr, total_send):
    if 0 <= ptr < len(insts):
        inst = insts[ptr]
        if inst[0] == "snd":
            send.append(val(inst[1], reg))
            total_send += 1
        elif inst[0] == "set":
            reg[inst[1]] = val(inst[2], reg)
        elif inst[0] == "add":
            reg[inst[1]] = reg.get(inst[1], 0) + val(inst[2], reg)
        elif inst[0] == "mul":
            reg[inst[1]] = reg.get(inst[1], 0) * val(inst[2], reg)
        elif inst[0] == "mod":
            reg[inst[1]] = reg.get(inst[1], 0) % val(inst[2], reg)
        elif inst[0] == "rcv":
            if recv:
                reg[inst[1]] = recv.pop(0)
            else:
                return send, recv, ptr, total_send
        elif inst[0] == "jgz":
            if val(inst[1], reg) > 0:
                ptr += val(inst[2], reg)
            else:
                ptr += 1
        if inst[0] != "jgz":
            ptr += 1
    else:
        return [], [], None, total_send
    return send, recv, ptr, total_send


def func2(data):
    insts = []
    for line in data.splitlines():
        parts = line.split()
        insts.append(parts)

    a_reg = {'p': 0}
    a_ptr = 0
    a_ptr2 = 0
    a_send = []
    b_reg = {'p': 1}
    b_ptr = 0
    b_ptr2 = 0
    b_send = []
    a_totalsent = 0
    b_totalsent = 0
    while True:
        #print("a", a_reg, a_send, a_ptr, a_totalsent)
        #print("b", b_reg, b_send, b_ptr, b_totalsent)
        if a_ptr is not None:
            a_send, b_send, a_ptr2, a_totalsent = execute(insts, a_reg, a_send, b_send, a_ptr, a_totalsent)
        if b_ptr is not None:
            b_send, a_send, b_ptr2, b_totalsent = execute(insts, b_reg, b_send, a_send, b_ptr, b_totalsent)
        if a_ptr2 == a_ptr and b_ptr2 == b_ptr:
            print("Both programs waiting / terminated")
            break
        a_ptr = a_ptr2
        b_ptr = b_ptr2
    return a_totalsent, b_totalsent

print(func2(example2))
print(func2(data))