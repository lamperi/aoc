import os.path
from itertools import pairwise

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def parse(data):
    rep = []
    for line in data.splitlines():
        v = tuple(int(i) for i in line.split())
        rep.append(v)
    return rep


def is_safe(r):
    return all((1 <= b-a  <= 3) for a, b in pairwise(r))


def is_part1_safe(r):
    if is_safe(r):
        return True
    r = tuple(reversed(r))
    if is_safe(r):
        return True
    return False


def part1(data):
    rep = parse(data)
    
    safe = 0
    for r in rep:
        if is_part1_safe(r):
            safe += 1
    return safe

test = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""
print(part1(test))
print(part1(data))

def part2(data):
    rep = parse(data)
    
    safe = 0
    for re in rep:
        if is_part1_safe(re):
            safe += 1
            continue

        # Problem Dampener
        for i, _ in enumerate(re):
            r = re[:i] + re[i+1:]
            if is_part1_safe(r):
                safe += 1
                break
    return safe

print(part2(test))
print(part2(data))