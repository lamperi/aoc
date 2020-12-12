import os.path
import collections
import re
import math
import itertools
INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

def create_prog(data):
    prog = []
    for line in data.split("\n"):
        if not line:
            break
        d = line[0]
        l = int(line[1:])
        prog.append((d, l))
    return prog

def next_left(dir):
    return {"E": "N", "N": "W", "W": "S", "S": "E"}[dir]

def next_right(dir):
    return {"E": "S", "S": "W", "W": "N", "N": "E"}[dir]

def solve(data):
    prog = create_prog(data)
    d = 'E'
    loc = [0, 0]
    for dir, l in prog:
        if dir == "N":
            loc[0] += l
        elif dir == "S":
            loc[0] -= l
        elif dir == "E":
            loc[1] += l
        elif dir == "W":
            loc[1] -= l
        elif dir == "L":
            for _ in range(int(l/90)):
                d = next_left(d)
        elif dir == "R":
            for _ in range(int(l/90)):
                d = next_right(d)
        elif dir == "F":
            if d == "N":
                loc[0] += l
            elif d == "S":
                loc[0] -= l
            elif d == "E":
                loc[1] += l
            elif d == "W":
                loc[1] -= l
        else:
            print("apua", dir, l)
    return abs(loc[0]) + abs(loc[1])

print(solve("""F10
N3
F7
R90
F11
"""), 25)
print(solve(data))

def solve2(data):
    prog = create_prog(data)
    wp_loc = [1, 10]
    ship_loc = [0, 0]
    for dir, l in prog: 
        if dir == "N":
            wp_loc[0] += l
        elif dir == "S":
            wp_loc[0] -= l
        elif dir == "E":
            wp_loc[1] += l
        elif dir == "W":
            wp_loc[1] -= l
        elif dir == "L":
            for _ in range(int(l/90)):
                dy =   wp_loc[0]
                dx =   wp_loc[1]
                wp_loc[0] =  + dx
                wp_loc[1] =  - dy
        elif dir == "R":
            for _ in range(int(l/90)):
                dy =   wp_loc[0]
                dx =   wp_loc[1]
                wp_loc[0] =  - dx
                wp_loc[1] =  + dy
        elif dir == "F":
            for _ in range(l):
                ship_loc[0] += wp_loc[0]
                ship_loc[1] += wp_loc[1]
        else:
            print("apua", dir, l)
    return abs(ship_loc[0]) + abs(ship_loc[1])

print(solve2("""F10
N3
F7
R90
F11
"""), 286)
print(solve2(data))
