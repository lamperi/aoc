import os.path
from itertools import pairwise

FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(FILE) as f:
    INPUT = f.read()

TEST = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

def draw(sand, walls, max_y):
    min_x = min(x for x,_ in walls | sand)
    max_x = max(x for x,_ in walls | sand)
    min_y = 0

    s = ""
    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            if (x,y) in walls:
                s += "#"
            elif (x,y) in sand:
                s += "o"
            else:
                s += "."
        s += "\n"
    print(s)

def solve(data, *, part):
    walls = set()
    for line in data.splitlines():
        coords = [
            tuple(map(int, p.split(",")))
            for p in line.split(" -> ")
        ]
        for a,b in pairwise(coords):
            for x in range(min(a[0], b[0]), max(a[0], b[0])+1):
                for y in range(min(a[1], b[1]), max(a[1], b[1])+1):
                    walls.add((x,y))
    sand = set()
    max_y = max(y for _,y in walls)
    # Endless wall is only part 2 but we can still keep it here for part 1.
    endless_wall = max_y + 2
    if part == 2:  # part 2
        # Allow sand to reach the endless wall.
        max_y += 2
    while True:
        # Source of sand is known to be 500, x
        x=500
        y=0
        sand_added = False
        while y <= max_y:
            if (x,y+1) not in walls and (x,y+1) not in sand and y+1 < endless_wall:
                y += 1
                continue
            elif (x-1, y+1) not in walls and (x-1, y+1) not in sand and y+1 < endless_wall:
                y += 1
                x -= 1
                continue
            elif (x+1, y+1) not in walls and (x+1, y+1) not in sand and y+1 < endless_wall:
                y += 1
                x += 1
                continue
            else:
                if (x,y) not in sand:
                    sand.add((x, y))
                    sand_added = True
                break
        if not sand_added:
            break
    #draw(static_sand, walls, max_y)
    return len(sand)

print(solve(TEST, part=1))
print(solve(INPUT, part=1))

print(solve(TEST, part=2))
print(solve(INPUT, part=2))

