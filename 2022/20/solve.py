import os.path
from itertools import pairwise
from dataclasses import dataclass
import re

FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(FILE) as f:
    INPUT = f.read()

def ints(line):
    return map(int, re.findall("-?\d+", line))

TEST = """1
2
-3
3
-2
0
4"""

def list_based_shuffle(n, *, repeat):
    # We need to uniqify all the elements:
    # There may be duplicates in the list.
    # Store as tuple: (original index, value)
    n = [(i,k) for i,k in enumerate(n)]
    n_order = n.copy()

    for _ in range(repeat):
        for i,k in n_order:
            ik = n.index((i,k))
            nik = (ik + k) % (len(n) - 1)
            del n[ik]
            n.insert(nik, (i,k))

    # We don't know the ID of the element with value 0.
    tuple0 = next((i,k) for i,k in n if k == 0)
    i0 = n.index(tuple0)
    a = n[(i0 + 1000)%(len(n))][1]
    b = n[(i0 + 2000)%(len(n))][1]
    c = n[(i0 + 3000)%(len(n))][1]
    return a+b+c

def solve(data):
    n = list(map(int, data.splitlines()))
    return list_based_shuffle(n.copy(), repeat=1)

def solve2(data):
    n = list(map(int, data.splitlines()))
    n = [k * 811589153 for k in n]
    return list_based_shuffle(n, repeat=10)

print(solve(TEST))
print(solve(INPUT))

print(solve2(TEST))
print(solve2(INPUT))
