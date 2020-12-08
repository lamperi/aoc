import os.path
import collections
import re
import math
INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

def run_prog(prog):
    acc = 0
    pc = 0
    vis = set()
    while True:
        if pc in vis:
            return acc, pc
        vis.add(pc)
        inst, arg = prog[pc]
        if inst == "acc":
            acc += arg
            pc += 1
        elif inst == "nop":
            pc += 1
        elif inst == "jmp":
            pc += arg
        if pc >= len(prog) or pc < 0:
            return acc, pc

def solve(data):
    prog = []
    for line in data.split("\n"):
        if not line:
            break
        inst, arg = line.split()
        arg = int(arg)
        prog.append((inst, arg))
    p1 = run_prog(prog)[0]
    for i, (inst, arg) in enumerate(prog):
        if inst == "jmp":
            prog_copy = prog[:]
            prog_copy[i] = ("nop", arg)
            acc, pc = run_prog(prog_copy)
            if pc >= len(prog_copy):
                p2 = acc
                break
        elif inst == "nop":
            prog_copy = prog[:]
            prog_copy[i] = ("jmp", arg)
            acc, pc = run_prog(prog_copy)
            if pc >= len(prog_copy):
                p2 = acc
                break
    return p1, p2

print(solve("""nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
"""))

print(solve(data))
