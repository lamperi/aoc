import os.path
import collections
import re
import math
INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

def solve(data):
    groups = []
    for group in data.split("\n\n"):
        groups.append([set(line) for line in group.splitlines()])
    s1 = 0
    s2 = 0
    for g in groups:
        s1 += len(set.union(*g))
        s2 += len(set.intersection(*g))
    return s1, s2

print(solve("""abc

a
b
c

ab
ac

a
a
a
a

b"""))
print(solve(data))
