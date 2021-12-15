from io import TextIOBase
import os.path
import operator
from itertools import combinations, pairwise, permutations
from functools import reduce, partial
from math import isfinite, prod
from collections import Counter, defaultdict
import re
from heapq import heappush, heappop

INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

test="""1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""

def solve(cavern):
    start=(0,0)
    end=(len(cavern)-1, len(cavern[0])-1)
    q=[(0, start)]
    visited={start}
    while q:
        d,(y,x)=heappop(q)
        for yd,xd in ((-1,0),(0,-1),(1,0),(0,1)):
            ny=y+yd
            nx=x+xd
            if not (0 <= ny <= end[0] and 0 <= nx <= end[1]):
                continue
            if (ny,nx) in visited:
                continue
            else:
                nd = d+cavern[ny][nx]
                if (ny,nx) == end:
                    return nd
                visited.add((ny,nx))
                heappush(q, (nd,(ny,nx)))

def part1(data):
    cavern = [[int(c) for c in s] for s in data.splitlines()]
    return solve(cavern)

print(part1(test))
print(part1(data))

def part2(data):
    cavern=[]
    lines=data.splitlines()
    for y in range(5):
        for line in lines:
            cave=[]
            cavern.append(cave)
            for x in range(5):
                for c in line:
                    cave.append((int(c) + y + x - 1)%9 + 1)
    return solve(cavern)

print(part2(test))
print(part2(data))

