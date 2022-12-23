import os.path
import re
from collections import defaultdict

def ints(line):
    return map(int, re.findall("-?\d+", line))


FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(FILE) as f:
    INPUT = f.read()

TEST = """....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#.."""

def check_north(elves, x, y):
    if not any(adj in elves for adj in ((x-1, y-1), (x,y-1), (x+1, y-1))):
        return x, y-1

def check_south(elves, x, y):
    if not any(adj in elves for adj in ((x-1, y+1), (x, y+1), (x+1, y+1))):
        return x, y+1

def check_west(elves, x, y):
    if not any(adj in elves for adj in ((x-1, y-1), (x-1, y), (x-1, y+1))):
        return x-1, y

def check_east(elves, x, y):
    if not any(adj in elves for adj in ((x+1, y-1), (x+1, y), (x+1, y+1))):
        return x+1, y
    
def print_elves(elves):
    min_x = min(x for x,y in elves)
    max_x = max(x for x,y in elves)
    min_y = min(y for x,y in elves)
    max_y = max(y for x,y in elves)
    s = ""
    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            if (x,y) not in elves:
                s += "."
            else:
                s += "#"
        s += "\n"
    print(s)

def solve(data):
    map = data.splitlines()

    elves = set()
    for y, row in enumerate(map):
        for x, c in enumerate(row):
            if c == "#":
                elves.add((x,y))
    #print_elves(elves)

    checks = [check_north, check_south, check_west, check_east]

    part1_res = None
    for t in range(1, 10000000):
        moves = defaultdict(list)
        for elf in elves:
            x, y = elf
            # Elves don't move if there's any neighbor
            found = False
            for adj in (
                (x-1, y-1), (x,y-1), (x+1, y-1),
                (x-1, y), (x+1, y),
                (x-1, y+1), (x, y+1), (x+1, y+1),
            ):
                if adj in elves:
                    found = True
                    break
            if not found:
                continue

            for check in checks:
                if n := check(elves, x, y):
                    moves[n].append(elf)
                    break

        move_count = 0
        for coord, sources in moves.items():
            if len(sources) == 1:
                elves.remove(sources[0])
                elves.add(coord)
                move_count += 1
        if move_count == 0:
            return part1_res, t

        # Rotate checks
        checks.append(checks.pop(0))
        #print_elves(elves)

        # Part 1
        if t == 10:
            min_x = min(x for x,y in elves)
            max_x = max(x for x,y in elves)
            min_y = min(y for x,y in elves)
            max_y = max(y for x,y in elves)

            s = 0
            for x in range(min_x, max_x+1):
                for y in range(min_y, max_y+1):
                    if (x,y) not in elves:
                        s += 1
            part1_res = s

print(solve(TEST))
print(solve(INPUT))
