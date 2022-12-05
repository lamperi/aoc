import os.path
import operator
import re
from itertools import combinations, permutations, pairwise
from functools import reduce, partial
from math import prod
import string
from collections import deque

FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(FILE) as f:
    INPUT = f.read()

TEST = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

def ints(line):
    return map(int, re.findall("\d+", line))

def chars(line):
    return map(int, re.findall("[A-Z]+", line))

def solve(data, part):
    assert part in (1,2)
    crane_stacks = {}
    for line in data.splitlines():
        # SETUP
        if "[" in line:
            for i,c in enumerate(line):
                if c in string.ascii_uppercase:
                    j = 1+((i-1)/4)
                    if j not in crane_stacks:
                        crane_stacks[j] = list()
                    crane_stacks[j].insert(0, c)
        # INST
        if "move" in line:
            n,f,t = ints(line)
            if part == 1:
                for k in range(n):
                    c = crane_stacks[f].pop()
                    crane_stacks[t].append(c)                
            elif part == 2:
                cs = crane_stacks[f][-n:]
                del crane_stacks[f][-n:]
                crane_stacks[t] += cs
    s = "".join(crane_stacks[k][-1] for k in sorted(crane_stacks.keys()))
    return s

print(solve(TEST, part=1))
print(solve(INPUT, part=1))
print(solve(TEST, part=2))
print(solve(INPUT, part=2))
