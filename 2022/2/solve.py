import os.path
import operator
from itertools import combinations, permutations, pairwise
from functools import reduce, partial
from math import prod

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

TEST = """A Y
B X
C Z"""

def solve(data):
    score = 0
    for line in data.splitlines():
        elf, me = line.split()
        if me == "X":
            score += 1
            if elf == "A":
                score += 3
            if elf == "C":
                score += 6
        if me == "Y":
            score += 2
            if elf == "B":
                score += 3
            if elf == "A":
                score += 6
        if me == "Z":
            score += 3
            if elf == "C":
                score += 3
            if elf == "B":
                score += 6
    return score

print(solve(TEST))
print(solve(data))

def solve2(data):
    score = 0
    for line in data.splitlines():
        elf, me = line.split()
        if me == "X":
            score += 0
            if elf == "A":
                score += 3
            if elf == "B":
                score += 1
            if elf == "C":
                score += 2
        if me == "Y":
            score += 3
            if elf == "A":
                score += 1
            if elf == "B":
                score += 2
            if elf == "C":
                score += 3        
        if me == "Z":
            score += 6
            if elf == "A":
                score += 2
            if elf == "B":
                score += 3
            if elf == "C":
                score += 1   
    return score

print(solve2(TEST))
print(solve2(data))