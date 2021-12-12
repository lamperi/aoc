from io import TextIOBase
import os.path
import operator
from itertools import combinations, permutations
from functools import reduce, partial
from math import isfinite, prod
from collections import Counter

INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

test="""2199943210
3987894921
9856789892
8767896789
9899965678"""

def get_adj(m, j, i):
    if i > 0:
        yield (j,i-1),int(m[j][i-1])
    if i < len(m[j])-1:
        yield (j,i+1),int(m[j][i+1])
    if j > 0:
        yield (j-1,i),int(m[j-1][i])
    if j < len(m)-1:
        yield (j+1,i),int(m[j+1][i])

def get_low_points(m):
    for j, row in enumerate(m):
        for i, c in enumerate(row):
            c = int(c)
            if all(n > c for _,n in get_adj(m,j,i)):
                yield (j,i),c

def part1(data):
    return sum(1+v for _,v in get_low_points(data.splitlines()))

print(part1(test))
print(part1(data))

def part2(data):
    m = data.splitlines()
    low_points = [p for p,_ in get_low_points(m)]
    visited = set()
    all_basis=[]
    for p in low_points:
        assert p not in visited
        visited.add(p)
        q = [p]
        basis = set([p])
        while q:
            p = q.pop(0)
            for pn,n in get_adj(m, *p):
                if n == 9:
                    continue
                if pn in visited:
                    continue
                visited.add(pn)
                basis.add(pn)
                q.append(pn)
        all_basis.append(len(basis))
    
    all_basis.sort()
    return prod(all_basis[-3:])

print(part2(test))
print(part2(data))

