from io import TextIOBase
import os.path
import operator
from itertools import combinations, permutations
from functools import reduce, partial
from math import prod
from collections import Counter

INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

test="""0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""

def points(c1,c2,diag):
    xd=c1[0]-c2[0]
    yd=c1[1]-c2[1]
    assert abs(xd)==abs(yd) or xd==0 or yd==0
    r=max(abs(xd), abs(yd))
    if not diag and xd != 0 and yd != 0:
        return
    if xd != 0:
        xd = 1 if xd > 0 else -1
    if yd != 0:
        yd = 1 if yd > 0 else -1
    p = c1[0], c1[1]
    for j in range(r):
        yield p
        p = p[0]-xd, p[1]-yd
    yield p

def solve(data, diag):
    v=[]
    for line in data.splitlines():
        c1,c2=line.split(" -> ")
        c1=[int(i) for i in c1.split(",")]
        c2=[int(i) for i in c2.split(",")]
        v.append((c1,c2))
    m = {}
    for c1, c2 in v:
        for p in points(c1, c2, diag):
            if p not in m:
                m[p] = 1
            else:
                m[p] += 1
    s=0
    for p,v in m.items():
        if v > 1:
            s+=1
    return s

def part1(data):
    return solve(data, False)

print(part1(test))
print(part1(data))

def part2(data):
    return solve(data, True)

print(part2(test))
print(part2(data))

