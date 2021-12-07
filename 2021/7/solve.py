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

test="""16,1,2,0,4,2,7,1,2,14"""

def solve(data, weight):
    c = [int(s) for s in data.split(",")]
    min_s=None
    for i in range(min(c), max(c)+1):
        s=0
        for a in c:
            s+=weight(a,i)
        if min_s is None or s < min_s:
            min_s=s
    return min_s

def part1(data):
    return solve(data, lambda a, b: abs(a-b))

print(part1(test))
print(part1(data))

def d(a,b):
    n=abs(a-b)
    return n*(n+1)//2

def part2(data):
    return solve(data, d)

print(part2(test))
print(part2(data))

