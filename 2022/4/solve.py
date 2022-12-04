import os.path
import operator
import re
from itertools import combinations, permutations, pairwise
from functools import reduce, partial
from math import prod

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

TEST = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""

def solve(data):
    s = 0
    s2 = 0
    for line in data.splitlines():
        if not line.strip():
            return
        a,b,c,d = map(int, re.findall("\d+", line))
        if a <= c and b >= d or c <= a and d >= b:
            s += 1
        if a <= c and b >= c or c <= a and d >= a:
            s2 += 1
    return s, s2

print(solve(TEST))
print(solve(data))
