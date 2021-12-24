import operator
import os.path
import re
from collections import Counter, defaultdict
from functools import partial, reduce
from heapq import heappop, heappush
from io import TextIOBase
from itertools import combinations, pairwise, permutations
from math import isfinite, prod
import random

INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

def create_fun(data):
    prog = ["x = 0", "y = 0", "z = 0", "w = 0"]
    i = -1
    last_x_add = 0
    for line in data.splitlines():
        match line.split():
            case ["inp", a]:
                prog.append(f'{a} = next(inp)')
                i += 1
            case ["add", a, b]:
                if b != "0":
                   prog.append(f'{a} += {b}')
                if a == "x" and b not in "xyzw":
                    last_x_add = int(b)
            case ["mul", a, b]:
                if b != "1":
                    prog.append(f'{a} *= {b}')
            case ["div", a, b]:
                if b != "1":
                    prog.append(f'{a} //= {b}')
            case ["mod", a, b]:
                prog.append(f'if {a} < 0 or {b} <= 0:')
                prog.append(f'  raise ZeroDivisionError("mod")')
                prog.append(f'{a} %= {b}')
            case ["eql", a, b]:
                if a == "x" and b == "w":
                    if -24 <= last_x_add <= 9:
                        prog.append(f"yield ({i},z,x,w)")
                prog.append(f'{a} = 1 if {a} == {b} else 0')
    prog.append("yield (-1,z,x,w)")
    alu = "def run_alu(inp):\n" + "\n".join(" " + l for l in prog) 
    exec_locals = {}
    exec(alu, {}, exec_locals)
    return exec_locals["run_alu"]

def from_digits(digits):
    return int("".join(str(d) for d in digits))

def to_digits(n):
    return [int(c) for c in str(n)]

def find_monad(data, var, fit, inc):
    ok = False
    run_alu = create_fun(data)
    fit_index = [i for i,_,_,_ in run_alu(iter([9]*14)) if i != -1]
    while True:
        inp = var[:]
        for i,f in zip(fit_index, fit):
            inp.insert(i, f)
        while True:
            ok = True
            for i,z,x,w in run_alu(iter(inp)):
                if i == -1 and z == 0:
                    return "".join(str(i) for i in inp)
                elif x == w:
                    continue
                elif x != w and 1 <= x <= 9:
                    inp[i] = x
                    break
                ok = False
                break
            if not ok:
                break
        while True:
            var = to_digits(from_digits(var) + inc)
            if 0 not in var:
                break

def part1(data):
    return find_monad(data, var = [9,9,9,9,9,9,9],
        fit = [9,9,9,9,9,9,9], inc=-1)

def part2(data):
    return find_monad(data, var = [1,1,1,1,1,1,1],
        fit = [1,1,1,1,1,1,1], inc=1)

print(part1(data))
print(part2(data))