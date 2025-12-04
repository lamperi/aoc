import os.path

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()
INPUT = os.path.join(os.path.dirname(__file__), 'test_input.txt')
with open(INPUT) as f:
    test = f.read()

def parse_into_area(data):
    area = {}
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            area[(y,x)] = c
    return area

def neigh(yx):
    y, x = yx
    yield y-1, x-1,
    yield y-1, x
    yield y-1, x+1
    yield y, x-1
    yield y, x+1
    yield y+1, x-1,
    yield y+1, x
    yield y+1, x+1

def find_accessible_rolls(area):
    accessible = set()
    for yx, c in area.items():
        if c != "@":
            continue
        rolls = 0
        for nyx in neigh(yx):
            n = area.get(nyx, None)
            if n == "@":
                rolls += 1
        if rolls < 4:
            accessible.add(yx)
    return accessible

def part1(data):
    area = parse_into_area(data)
    accessible = find_accessible_rolls(area)
    return len(accessible)

print(part1(test))
print(part1(data))

def part2(data):
    area = parse_into_area(data)
    all_removed = set()
    while removed := find_accessible_rolls(area):
        for r in removed:
            area[r] = "."
        all_removed |= removed
    return len(all_removed)

print(part2(test))
print(part2(data))