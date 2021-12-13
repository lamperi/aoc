from io import TextIOBase
import os.path
import operator
from itertools import combinations, permutations
from functools import reduce, partial
from math import isfinite, prod
from collections import Counter
import re

INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

test="""6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""

def show_dots(d):
    max_y = max(y for y,_ in d)
    max_x = max(x for _,x in d)
    p=[
        ['#' if (y,x) in d else ' '
        for x in range(max_x+1)]
        for y in range(max_y+1)
    ]
    return ("\n".join("".join(s) for s in p))

def parse(data, line_parser, mapper):
    def convert_ints(d):
        return {
            k: (int(v) if v.isdigit() else v)
            for k, v in d.items()
        }
    return (mapper(convert_ints(
        re.search(line_parser, line).groupdict()))
        for line in data.splitlines())

def fold(data, part1=False):
    dots,inst = data.split("\n\n")
    dots=set(parse(dots,
        r'(?P<x>\d+),(?P<y>\d+)',
        lambda d: (d['y'], d['x'])))
    inst=parse(inst,
        r'.*(?P<ax>y|x)=(?P<c>\d+)',
        lambda d: (d['ax'], d['c']))
    for ax,c in inst:
        if ax == "y":
            dots = set((2*c-y,x) if y > c else (y,x) for y,x in dots)
        elif ax == "x":
            dots = set((y,2*c-x) if x > c else (y,x) for y,x in dots)
        if part1:
            return len(dots)
    return show_dots(dots)

def part1(data):
    return fold(data, part1=True)

print(part1(test))
print(part1(data))

def part2(data):
    return fold(data, part1=False)

print(part2(test))
print(part2(data))

