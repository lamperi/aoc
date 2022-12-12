import os.path
import re
import collections

FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(FILE) as f:
    INPUT = f.read()

TEST = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

def dist(a,b):
    # Special handling: if b == E
    # return 1 only for a == z.
    if b == "E":
        if a == "z":
            return 1
        else:
            return 2
    return ord(b) - ord(a)

def solve(data, part):
    map = data.splitlines()
    q = []
    visited = set()
    # PART1: Always start from 0,0
    if part == 1:
        q.append(((0,0), 'a', 0))
        visited.add((0,0))
    # PART2: Start from any elevation marked with a
    else:
        for i,row in enumerate(map):
            for j,c in enumerate(row):
                if c == "a":
                    q.append(((i,j), 'a', 0))
                    visited.add((i,j))
    while q:
        n,c,d = q.pop(0)
        for di,dj in ((-1,0),(0,1),(1,0),(0,-1)):
            m = n[0]+di,n[1]+dj
            if m not in visited and 0 <= m[0] < len(map) and 0 <= m[1] < len(map[m[0]]):
                e = map[m[0]][m[1]]
                if dist(c,e) <= 1:
                    if e == "E":
                        return d+1
                    visited.add(m)
                    q.append([m, e, d+1])

print(solve(TEST, part=1))
print(solve(INPUT, part=1))
print(solve(TEST, part=2))
print(solve(INPUT, part=2))

