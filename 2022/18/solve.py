import os.path
from itertools import pairwise
import re

FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(FILE) as f:
    INPUT = f.read()

def ints(line):
    return map(int, re.findall("-?\d+", line))

TEST = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""

def find_visible_cube_sides(lava):
    adj = {}
    for x,y,z in lava:
        adj[(x,y,z)] = []
        for xd,yd,zd in [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]:
            x2 = x+xd
            y2 = y+yd
            z2 = z+zd
            if (x2,y2,z2) in lava:
                adj[(x,y,z)].append((x2,y2,z2))
    visible = 0
    for a in adj.values():
        visible += 6 - len(a)
    return visible

def solve(data):
    lava = set()
    for line in data.splitlines():
        if not line.strip():
            continue
        x,y,z = ints(line)
        lava.add((x,y,z))
    res_part1 = find_visible_cube_sides(lava)

    # Find trapped:
    x_min = min(x for x,_,_ in lava)
    x_max = max(x for x,_,_ in lava)
    y_min = min(y for _,y,_ in lava)
    y_max = max(y for _,y,_ in lava)
    z_min = min(z for _,_,z in lava)
    z_max = max(z for _,_,z in lava)
    trapped = set()
    for (X,Y,Z) in gen_bounded_coordinates(lava):
        # IS this trapped?
        if (X,Y,Z) in lava:
            # Not air pocket
            continue
        # BFS again.
        q = [(X,Y,Z)]
        visited = set([X,Y,Z])
        while q:
            x,y,z = q.pop(0)
            if x < x_min or x > x_max or y < y_min or y > y_max or z < z_min or z > z_max:
                # If we can reach out, we are not air pocket.
                break
            for xd,yd,zd in [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]:
                x2 = x+xd
                y2 = y+yd
                z2 = z+zd
                if (x2,y2,z2) not in lava and (x2,y2,z2) not in visited:
                    q.append((x2,y2,z2))
                    visited.add((x2,y2,z2))
        # Only if the air was inside the lava area we are trapped.
        if not q:
            trapped.add((X,Y,Z))
    # Fill the trapped blocks with lava so calculatioin
    # from part 1 works here too.
    for c in trapped: 
        lava.add(c)
    # Returns (part1, part2) solution
    return res_part1, find_visible_cube_sides(lava)

def gen_bounded_coordinates(lava):
    x_min = min(x for x,_,_ in lava)
    x_max = max(x for x,_,_ in lava)
    y_min = min(y for _,y,_ in lava)
    y_max = max(y for _,y,_ in lava)
    z_min = min(z for _,_,z in lava)
    z_max = max(z for _,_,z in lava)
    for x in range(x_min, x_max+1):
        for y in range(y_min, y_max+1):
            for z in range(z_min, z_max+1):
                yield x,y,z

print(solve(TEST))
print(solve(INPUT))