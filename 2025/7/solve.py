import os.path
from collections import defaultdict

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()
INPUT = os.path.join(os.path.dirname(__file__), 'test_input.txt')
with open(INPUT) as f:
    test = f.read()

def parse(data):
    splitters = set()
    lines = data.splitlines()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == 'S':
                start = (y,x)
            elif c == '^':
                splitters.add((y,x))
    return start, splitters, len(lines)

def part1(data):
    start, splitters, height = parse(data)
    beam_ends = set([start])
    splits = 0
    for _ in range(0, height):
        new_beam_ends = set()
        for y,x in beam_ends:
            next_pos = y+1, x
            if next_pos not in splitters:
                new_beam_ends.add(next_pos)
            else:
                left = y+1,x-1
                right = y+1,x+1
                new_beam_ends.add(left)
                new_beam_ends.add(right)
                splits += 1
        beam_ends = new_beam_ends
    return splits

print(part1(test))
print(part1(data))

def part2(data):
    start, splitters, height = parse(data)
    beam_ends = {start: 1}
    for _ in range(0, height):
        new_beam_ends = defaultdict(int)
        for (y,x), possibilities in beam_ends.items():
            next_pos = y+1, x
            if next_pos not in splitters:
                new_beam_ends[next_pos] += possibilities
            else:
                left = y+1,x-1
                right = y+1,x+1
                new_beam_ends[left] += possibilities
                new_beam_ends[right] += possibilities
        beam_ends = new_beam_ends
    s = sum(beam_ends.values())
    return s

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))