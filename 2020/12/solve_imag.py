import os.path
import collections
import re
import math
import itertools
INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

def create_prog(data):
    return ((line[0], int(line[1:])) for line in data.splitlines())

DIRS = {"N": 1, "S": -1, "E": 1j, "W": -1j}
TURNS = {"L": -1j, "R": 1j}

def solve(data: str, wp_loc: complex, nswe_modifies_wp: bool):
    ship_loc = 0+0j
    for inst, arg in create_prog(data):
        if inst in "NSEW":
            if nswe_modifies_wp:
                wp_loc += DIRS[inst]*arg
            else:
                ship_loc += DIRS[inst]*arg
        elif inst in "LR":
            wp_loc *= TURNS[inst] ** int(arg/90)
        elif inst == "F":
            ship_loc += arg*wp_loc
        else:
            assert(False)
    return int(abs(ship_loc.real) + abs(ship_loc.imag))

def solve1(data):
    return solve(data, wp_loc=1j, nswe_modifies_wp=False)

print(solve1("""F10
N3
F7
R90
F11
"""), 25)
print(solve1(data))

def solve2(data):
    return solve(data, wp_loc=1+10j, nswe_modifies_wp=True)

print(solve2("""F10
N3
F7
R90
F11
"""), 286)
print(solve2(data))
