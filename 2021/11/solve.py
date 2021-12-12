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

test="""5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

def adj(o,i,j):
    for id,jd in ((-1,-1), (-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)):
        ii=i+id
        jj=j+jd
        if 0 <= ii < len(o) and 0 <= jj < len(o[ii]):
            yield ii,jj

def ints(t0):
    while True:
        yield t0
        t0 += 1

def simulate_dumbo_octopuses(data, steps):
    o = [[int(c) for c in line] for line in data.splitlines()]
    num_octopuses = sum(len(line) for line in o)
    total_flash=0
    for t in steps:
        for i, line in enumerate(o):
            for j, c in enumerate(line):
                o[i][j] += 1
        flashed=set()
        while True:
            new_flash=False
            for i, line in enumerate(o):
                for j, c in enumerate(line):
                    if c > 9 and (i,j) not in flashed:
                        flashed.add((i,j))
                        new_flash=True
                        total_flash+=1
                        for ii,jj in adj(o,i,j):
                            o[ii][jj]+=1
            if not new_flash:
                break
        for i, line in enumerate(o):
            for j, c in enumerate(line):
                if c > 9:
                    o[i][j] = 0
        if len(flashed) == num_octopuses:
            # part 2
            return t
    # part 1
    return total_flash          


def part1(data):
    return simulate_dumbo_octopuses(data, steps=range(100))         

print(part1(test))
print(part1(data))

def part2(data):
    return simulate_dumbo_octopuses(data, steps=ints(t0=1))

print(part2(test))
print(part2(data))

