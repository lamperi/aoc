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

test="""start-A
start-b
A-c
A-b
b-d
A-end
b-end"""


def dfs(cave, c, visited, visited_twice):
    if c == "end":
        return 1
    if c[0].lower()==c[0]:
        if c not in visited:
            visited = visited | set([c])
        else:
            visited_twice = True
    s = 0
    for a in cave[c]:
        if a == "start" or a in visited and visited_twice:
            continue
        s += dfs(cave, a, visited, visited_twice)
    return s

def parse_caves(data):
    caves={}
    for line in data.splitlines():
        start,end=line.split("-") 
        if start not in caves:
            caves[start] = []
        caves[start].append(end)
        if end not in caves:
            caves[end] = []
        caves[end].append(start)
    return caves

def part1(data):
    npaths=dfs(parse_caves(data), "start", set(), True)
    return npaths

print(part1(test))
print(part1(data))

def part2(data):
    npaths=dfs(parse_caves(data), "start", set(), False)
    return npaths

print(part2(test))
print(part2(data))

