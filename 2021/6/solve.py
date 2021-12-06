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

test="""3,4,3,1,2"""

def part1(data):
    # Unoptimized with full data structure.
    fish = [int(s) for s in data.split(",")]
    for t in range(80):
        fish.extend([9]*fish.count(0))
        fish = [f-1 if f>0 else 6 for f in fish]
    return len(fish)

print(part1(test))
print(part1(data))

def part2(data):
    # Optimized by only having a fish counter.
    fish = [int(s) for s in data.split(",")]
    fish_count = {i: 0 for i in range(9)}
    for f in fish:
        fish_count[f]+=1
    for t in range(256):
        fish_count_new = {i: fish_count.get(i+1,0) for i in range(9)}
        fish_count_new[6] += fish_count[0]
        fish_count_new[8] += fish_count[0]
        fish_count = fish_count_new
    return sum(fish_count.values())

print(part2(test))
print(part2(data))

