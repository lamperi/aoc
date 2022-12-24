import os.path
import re
from collections import deque
import heapq
import math

def ints(line):
    return map(int, re.findall("-?\d+", line))

FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(FILE) as f:
    INPUT = f.read()

TEST = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""

def step(area, blizzard, t):
    x, y, c = blizzard
    x -= 1
    y -= 1
    H = len(area)-2 if blizzard[2] in "^v" else len(area[0])-2
    if blizzard[2] == "<":
        new_x = (x - t) % H
        return new_x + 1, y + 1, c
    elif blizzard[2] == ">":
        new_x = (x + t) % H
        return new_x + 1, y + 1, c
    elif blizzard[2] == "^":
        new_y = (y - t) % H
        return x + 1, new_y + 1, c
    elif blizzard[2] == "v":
        new_y = (y + t) % H
        return x + 1, new_y + 1, c


def play(area, b, path):
    for t, p in enumerate(path):
        s = f"Minute {t}\n"
        for y, row in enumerate(area):
            for x, c in enumerate(row):
                if c in "<>^v.":
                    if p == (x,y):
                        s += "E"
                        continue
                    bb = []
                    for (bx,by,bc) in b:
                        if bx == x and by == y:
                            bb.append(bc)
                    if len(bb) > 1:
                        assert len(bb) < 10
                        s += str(len(bb))
                    elif len(bb) == 1:
                        s += bb[0]
                    else:
                        s += "."
                elif c in "#":
                    s += "#"
            s += "\n"
        print(s)
        b = [
            step(area, bb, 1) for bb in b
        ]

def solve2(data):
    area = data.splitlines()

    blizzards = []
    for y, row in enumerate(area):
        for x, c in enumerate(row):
            if c in "<>^v":
                blizzards.append((x,y,c))
    B = blizzards[:]

    # Calculate how often blizzards repeat state.
    # This way we can avoid infinite loops.
    r = len(area)-2, len(area[0])-2
    cycle_len = r[0]*r[1]//math.gcd(*r)
    assert B == [step(area, b, cycle_len) for b in B]

    start = (1, 0)  # x, y
    end = (len(area[-1])-2, len(area)-1)
    # New param om part2 to visited state: stage (0,1,2)
    visited = set()
    visited.add((start, 0, 0))

    FIRST_END = 0
    BACK_TO_START = 1
    SECOND_END = 2

    q = []
    q.append((0,0,start))

    i = 0
    skips = 0
    best = None
    best_part1 = None

    # Part 2: 25*120*600 states times 3.
    # 5.4M states to visit.
    precalc_blizzard = []
    for t in range(cycle_len):
        walls = frozenset((x,y) for x,y,_ in [
            step(area, b, t) for b in B
        ])
        precalc_blizzard.append(walls)

    while q:        
        L, stage, (x,y) = q.pop(0)
        i += 1
        blizzard_wall = precalc_blizzard[(L+1)%cycle_len]

        for adj in ((x+1, y), (x, y+1), (x-1, y), (x, y-1), (x,y)):
            new_stage = stage
            if not (0 <= adj[1] < len(area)) or area[adj[1]][adj[0]] == "#":
                continue
            elif adj in blizzard_wall:
                continue
            elif adj == end and stage in (FIRST_END, SECOND_END):
                if stage == SECOND_END:
                    if best is None:
                        best = L+1
                        return best_part1, best
                else:
                    new_stage += 1
                    if best_part1 is None:
                        best_part1 = L+1
                    else:
                        best_part1 = min(best_part1, L+1)
            elif adj == start and stage == BACK_TO_START:
                new_stage += 1

            unique_st = (adj, (L+1)%cycle_len, new_stage)
            if unique_st in visited:
                skips += 1
                continue
            visited.add(unique_st)

            st = L+1, new_stage, adj
            q.append(st)

    assert best is not None, "search terminated"
    return best_part1, best

print(solve2(TEST))
print(solve2(INPUT))