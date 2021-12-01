import os.path
import operator
from itertools import combinations, permutations
from functools import reduce, partial
from math import prod

INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

ints = [int(i) for i in data.splitlines()]

s=0
for i,j in zip(ints, ints[1:]):
    if j > i:
        s+=1
print(s)

s=0
for i,j,k,l in zip(ints, ints[1:], ints[2:], ints[3:]):
    if (i+j+k) < (j+k+l):
        s+=1
print(s)
