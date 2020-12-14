import os.path
import collections
import re
import math
import itertools
INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

def solve(data):
    inst = []
    for line in data.splitlines():
        command, value = line.split(" = ")
        inst.append((command, value))

    mask = ""
    mem = {}
    for cmd, val in inst:
        if cmd == "mask":
            mask = val
        elif cmd.startswith("mem"):
            addr = int(cmd.split("[")[1][:-1])
            val = int(val)
            for bit, b in enumerate(reversed(mask)):
                if b == "0":
                    val &= ~(1<<bit)
                elif b == "1":
                    val |= (1<<bit)
            mem[addr] = val
    return sum(mem.values())

print(solve("""mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""))
print(solve(data))

def solve2(data):
    inst = []
    for line in data.splitlines():
        command, value = line.split(" = ")
        inst.append((command, value))
    print(len(inst))
    mask = ""
    mem = {}
    for cmd, val in inst:
        if cmd == "mask":
            mask = val
        elif cmd.startswith("mem"):
            addrs = [int(cmd.split("[")[1][:-1])]
            val = int(val)
            for bit, b in enumerate(reversed(mask)):
                if b == "X":
                    addrs = [a & ~(1<<bit) for a in addrs] + [a | (1<<bit) for a in addrs] 
                elif b == "0":
                    pass
                elif b == "1":
                    addrs = [a | (1<<bit) for a in addrs] 
            for a in addrs:
                mem[a] = val
    return sum(mem.values())

print(solve2("""mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""))
print(solve2(data))