import operator
import os.path
import re
from collections import Counter, defaultdict
from functools import partial, reduce
from heapq import heappop, heappush
from io import TextIOBase
from itertools import combinations, pairwise, permutations
from math import isfinite, prod

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

test = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""


def print_area(area):
    max_y = max(y for y, _ in area)+1
    max_x = max(x for _, x in area)+1
    s = ''
    for y in range(0, max_y):
        for x in range(0, max_x):
            s += area[(y, x)]
        s += '\n'
    print(s)


def part1(data):
    area = {}
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            area[(y, x)] = c
    max_y = max(y for y, _ in area)+1
    max_x = max(x for _, x in area)+1

    for t in range(1, 100000):
        moves = 0
        new_area = area.copy()
        east_facing = sorted((-k[1], k) for k, v in area.items() if v == '>')
        for _, (y, x) in east_facing:
            if area[(y, (x+1) % max_x)] == '.':
                new_area[(y, (x+1) % max_x)] = '>'
                new_area[(y, x)] = '.'
                moves += 1
        area = new_area
        new_area = area.copy()
        south_facing = sorted((-k[0], k) for k, v in area.items() if v == 'v')
        for _, (y, x) in south_facing:
            if area[((y+1) % max_y, x)] == '.':
                new_area[((y+1) % max_y, x)] = 'v'
                new_area[(y, x)] = '.'
                moves += 1
        if moves == 0:
            return t
        area = new_area
    return False


print(part1(test))
print(part1(data))
