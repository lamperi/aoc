import os.path
import operator
from itertools import combinations, permutations, pairwise
from functools import reduce, partial
from math import prod

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

TEST = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

def solve(data):
    score = 0
    for line in data.splitlines():
        a,b = line[:len(line)//2], line[len(line)//2:]
        c = ((set(a)&set(b)))
        assert len(c) == 1
        c = next(iter(c))
        if c.isupper():
            p = ord(c) - ord('A') + 27
        else:
            p = ord(c) - ord('a') + 1
        score += p
    return score

print(solve(TEST))
print(solve(data))

def solve2(data):
    score = 0
    lines = data.splitlines()
    for i in range(0, len(lines), 3):
        a,b,d = lines[i:i+3]
        c = ((set(a)&set(b)&set(d)))
        assert len(c) == 1
        c = next(iter(c))
        if c.isupper():
            p = ord(c) - ord('A') + 27
        else:
            p = ord(c) - ord('a') + 1
        score += p
    return score

print(solve2(TEST))
print(solve2(data))

