import os.path
import collections
import re
import math
import itertools
INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

def adj(z,y,x):
    for zz in (z-1, z, z+1):
        for yy in (y-1, y, y+1):
            for xx in (x-1, x, x+1):
                if zz != z or yy != y or xx != x:
                    yield zz, yy, xx

def solve(data):
    space = {0: {}}
    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0
    min_z = 0
    max_z = 0
    for y, line in enumerate(data.splitlines()):
        space[0][y] = {}
        if y > max_y:
            max_y = y
        for x, c in enumerate(line):
            space[0][y][x] = c
            if x > max_x:
                max_x = x

    for cycle in range(1,7):
        next_space = {}
        for z in range(min_z-1, max_z+2):
            next_space[z] = {}
            for y in range(min_y-1, max_y+2):
                next_space[z][y] = {}
                for x in range(min_x-1, max_x+2):
                    cur = space.get(z, {}).get(y, {}).get(x, ".")
                    active_adj = 0
                    inactive_adj = 0
                    for zz, yy, xx in adj(z,y,x):
                        if space.get(zz, {}).get(yy, {}).get(xx, ".") == ".":
                            inactive_adj += 1
                        else:
                            active_adj += 1
                    if cur == "." and active_adj == 3:
                        if z not in next_space:
                            next_space[z] = {}
                        if y not in next_space[z]:
                            next_space[z][y] = {}
                        next_space[z][y][x] = "#"
                    elif cur == "#" and active_adj not in (2,3):
                        if z not in next_space:
                            next_space[z] = {}
                        if y not in next_space[z]:
                            next_space[z][y] = {}
                        next_space[z][y][x] = "."
        for z in next_space.keys():
            for y in next_space[z].keys():
                if z not in space:
                    space[z] = {}
                if y not in space[z]:
                    space[z][y] = {}
                space[z][y].update(next_space[z][y])

        min_z = 0
        max_z = 0
        min_y = 10
        max_y = 0
        min_x = 10
        max_x = 0
        for z in sorted(space.keys()):
            for y in range(min(space[z])-1, max(space[z])+2):
                if y not in space[z] or len(space[z][y]) == 0:
                    continue
                for x in range(min(space[z][y])-1, max(space[z][y])+2):
                    cube = space.get(z, {}).get(y, {}).get(x, ".")
                    if cube == "#":
                        min_z = min(z, min_z)
                        min_y = min(y, min_y)
                        min_x = min(x, min_x)
                        max_z = max(z, max_z)
                        max_y = max(y, max_y)
                        max_x = max(x, max_x)
        if None: # Detailed print
            print("CYCLE", cycle)
            for z in range(min_z, max_z+1):
                print("z={}".format(z))
                lines = []
                for y in range(min_y, max_y+1):
                    line = []
                    for x in range(min_x, max_x+1):
                        cube = space.get(z, {}).get(y, {}).get(x, ".")
                        line.append(cube)
                    lines.append("".join(line))
                print("\n".join(lines))
                print()
            active = 0
            for zdim in space.values():
                for ydim in zdim.values():
                    for cube in ydim.values():
                        if cube == "#":
                            active += 1
            print("active: {}\n".format(active))

    active = 0
    for zdim in space.values():
        for ydim in zdim.values():
            for cube in ydim.values():
                if cube == "#":
                    active += 1
    return active

print(solve(""".#.
..#
###"""))
print(solve(data))


def adj2(w, z,y,x):
    for ww in (w-1, w, w+1):
        for zz in (z-1, z, z+1):
            for yy in (y-1, y, y+1):
                for xx in (x-1, x, x+1):
                    if ww != w or zz != z or yy != y or xx != x:
                        yield ww, zz, yy, xx
def solve2(data):
    space = {0: {0: {}}}
    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0
    min_z = 0
    max_z = 0
    min_w = 0
    max_w = 0
    for y, line in enumerate(data.splitlines()):
        space[0][0][y] = {}
        if y > max_y:
            max_y = y
        for x, c in enumerate(line):
            space[0][0][y][x] = c
            if x > max_x:
                max_x = x

    for cycle in range(1,7):
        next_space = {}
        for w in range(min_w-1, max_w+2):
            next_space[w] = {}
            for z in range(min_z-1, max_z+2):
                next_space[w][z] = {}
                for y in range(min_y-1, max_y+2):
                    next_space[w][z][y] = {}
                    for x in range(min_x-1, max_x+2):
                        cur = space.get(w, {}).get(z, {}).get(y, {}).get(x, ".")
                        active_adj = 0
                        inactive_adj = 0
                        for ww, zz, yy, xx in adj2(w, z,y,x):
                            if space.get(ww, {}).get(zz, {}).get(yy, {}).get(xx, ".") == ".":
                                inactive_adj += 1
                            else:
                                active_adj += 1
                        if cur == "." and active_adj == 3:
                            if w not in next_space:
                                next_space[w] = {}
                            if z not in next_space[w]:
                                next_space[w][z] = {}
                            if y not in next_space[w][z]:
                                next_space[w][z][y] = {}
                            next_space[w][z][y][x] = "#"
                        elif cur == "#" and active_adj not in (2,3):
                            if w not in next_space:
                                next_space[w] = {}
                            if z not in next_space[w]:
                                next_space[w][z] = {}
                            if y not in next_space[w][z]:
                                next_space[w][z][y] = {}
                            next_space[w][z][y][x] = "."
        for w in next_space.keys():
            for z in next_space[w].keys():
                for y in next_space[w][z].keys():
                    if w not in space:
                        space[w] = {}
                    if z not in space[w]:
                        space[w][z] = {}
                    if y not in space[w][z]:
                        space[w][z][y] = {}
                    space[w][z][y].update(next_space[w][z][y])

        min_w = 0
        max_w = 0
        min_z = 0
        max_z = 0
        min_y = 10
        max_y = 0
        min_x = 10
        max_x = 0
        for w in sorted(space.keys()):
            for z in range(min(space[w])-1, max(space[w])+2):
                if z not in space[w] or len(space[w][z]) == 0:
                        continue
                for y in range(min(space[w][z])-1, max(space[w][z])+2):
                    if y not in space[w][z] or len(space[w][z][y]) == 0:
                        continue
                    for x in range(min(space[w][z][y])-1, max(space[w][z][y])+2):
                        cube = space.get(w, {}).get(z, {}).get(y, {}).get(x, ".")
                        if cube == "#":
                            min_w = min(w, min_w)
                            max_w = max(w, max_w)
                            min_z = min(z, min_z)
                            min_y = min(y, min_y)
                            min_x = min(x, min_x)
                            max_z = max(z, max_z)
                            max_y = max(y, max_y)
                            max_x = max(x, max_x)
        if None: # debug
            print("CYCLE", cycle)
            active = 0
            for wdim in space.values():
                for zdim in wdim.values():
                    for ydim in zdim.values():
                        for cube in ydim.values():
                            if cube == "#":
                                active += 1
            print("active: {}\n".format(active))

    active = 0
    for wdim in space.values():
        for zdim in wdim.values():
            for ydim in zdim.values():
                for cube in ydim.values():
                    if cube == "#":
                        active += 1
    return active

print(solve2(""".#.
..#
###"""))
print(solve2(data))