import os.path
from itertools import combinations
import sys
self_test = "--self-test" in sys.argv

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    data = f.read()

with open(os.path.join(os.path.dirname(__file__), "test1.txt")) as f:
    test = f.read()

with open(os.path.join(os.path.dirname(__file__), "test2.txt")) as f:
    test2 = f.read()

with open(os.path.join(os.path.dirname(__file__), "test3.txt")) as f:
    test3 = f.read()

def part1(data):
    inputs = []
    for line in data.splitlines():
        cmd, coords = line.split()
        x,y,z=coords.split(",")
        x = [int(n) for n in x.split("=")[1].split("..")]
        y = [int(n) for n in y.split("=")[1].split("..")]
        z = [int(n) for n in z.split("=")[1].split("..")]
        inputs.append((cmd, x, y, z))
    on=set()
    for cmd, (min_x, max_x), (min_y, max_y), (min_z, max_z) in inputs:
        min_x = max(-50, min_x)
        max_x = min(50, max_x)
        min_y = max(-50, min_y)
        max_y = min(50, max_y)
        min_z = max(-50, min_z)
        max_z = min(50, max_z)
        for x in range(min_x, max_x+1):
            for y in range(min_y, max_y+1):
                for z in range(min_z, max_z+1):
                    if cmd == "on":
                        on.add((x,y,z))
                    elif cmd == "off" and (x,y,z) in on:
                        on.remove((x,y,z))
    return len(on)

if self_test:
    assert(part1(test) == 39)
    assert(part1(test2) == 590784)
print(part1(data))

def axis_intersection(min_x, max_x, min_x2, max_x2):
    return ((max_x >= min_x2 and min_x <= min_x2)
        or max_x2 >= min_x and min_x2 <= min_x)

def intersection(cube1, cube2):
    (min_x, max_x), (min_y, max_y), (min_z, max_z) = cube1
    (min_x2, max_x2), (min_y2, max_y2), (min_z2, max_z2) = cube2
    return (axis_intersection(min_x, max_x, min_x2, max_x2)
        and axis_intersection(min_y, max_y, min_y2, max_y2)
        and axis_intersection(min_z, max_z, min_z2, max_z2))

def get_shapes(cube1, cube2, test=False):
    # make cube2 into smaller rectangular pieces
    shapes = []
    (min_x, max_x), (min_y, max_y), (min_z, max_z) = cube1
    (min_x2, max_x2), (min_y2, max_y2), (min_z2, max_z2) = cube2
    if min_x <= min_x2 and max_x >= min_x2:
        if max_x < max_x2:
            shapes.append(((max_x+1, max_x2), (min_y2, max_y2), (min_z2, max_z2)))
            max_x2 = max_x
    if min_x2 < min_x and max_x2 >= min_x:
        shapes.append(((min_x2, min_x-1), (min_y2, max_y2), (min_z2, max_z2)))
        min_x2 = min_x
    if max_x2 >= max_x and min_x2 <= max_x:
        if max_x+1 <= max_x2:
            shapes.append(((max_x+1, max_x2), (min_y2, max_y2), (min_z2, max_z2)))
            max_x2 = max_x
    if min_y <= min_y2 and max_y >= min_y2:
        if max_y < max_y2:
            shapes.append(((min_x2, max_x2), (max_y+1, max_y2), (min_z2, max_z2)))
            max_y2 = max_y
    if min_y2 < min_y and max_y2 >= min_y:
        shapes.append(((min_x2, max_x2), (min_y2, min_y-1), (min_z2, max_z2)))
        min_y2 = min_y
    if max_y2 >= max_y and min_y2 <= max_y:
        if max_y+1 <= max_y2:
            shapes.append(((min_x2, max_x2), (max_y+1, max_y2), (min_z2, max_z2)))
            max_y2 = max_y
    if min_z <= min_z2 and max_z >= min_z2:
        if max_z < max_z2:
            shapes.append(((min_x2, max_x2), (min_y2, max_y2), (max_z+1, max_z2)))
        max_z2 = max_z
    if min_z2 < min_z and max_z2 >= min_z:
        shapes.append(((min_x2, max_x2), (min_y2, max_y2), (min_z2, min_z-1)))
        min_z2 = min_z
    if max_z2 >= max_z and min_z2 <= max_z:
        if max_z+1 <= max_z2:
            shapes.append(((min_x2, max_x2), (min_y2, max_y2), (max_z+1, max_z2)))
            max_z2 = max_z
    if test:
        if min_x2 <= max_x2 and min_y2 <= max_y2 and min_z2 <= max_z2:
            assert intersection(cube1, ((min_x2, max_x2), (min_y2, max_y2), (min_z2, max_z2)))
        for s1, s2 in combinations(shapes, 2):
            assert not intersection(s1, s2), f"{s1} and {s2}"
        for s in shapes:
            assert not intersection(cube1, s), f"{cube1} and {s}"
            for ax in s:
                assert ax[1] >= ax[0], f"{s}"
        a1 = get_init_area([cube1, cube2]) 
        a2 = get_init_area(shapes + [cube1])
        if a1 != a2:
            print("compare", count_init_area(shapes + [cube1]), count_init_area([cube1, cube2]))
            print("missing", list(a1 - a2)[:10])
            print("extra", list(a2 - a1)[:10])
        assert count_init_area(shapes + [cube1]) == count_init_area([cube1, cube2]), f"failed for {cube1} and {cube2}: {shapes}"
    return shapes


def get_pixels(cubes):
    pixels_on = 0
    for (min_x, max_x), (min_y, max_y), (min_z, max_z) in cubes:
        pixels_on += abs(1 + max_x - min_x) * abs(1 + max_y - min_y) * abs(1 + max_z - min_z)
    return pixels_on

def get_init_area(cubes):
    on=set()
    for (min_x, max_x), (min_y, max_y), (min_z, max_z) in cubes:
        min_x = max(-50, min_x)
        max_x = min(50, max_x)
        min_y = max(-50, min_y)
        max_y = min(50, max_y)
        min_z = max(-50, min_z)
        max_z = min(50, max_z)
        for x in range(min_x, max_x+1):
            for y in range(min_y, max_y+1):
                for z in range(min_z, max_z+1):
                    on.add((x,y,z))
    return on

def count_init_area(cubes):
    return len(get_init_area(cubes))


def part2(data):
    inputs = []
    for line in data.splitlines():
        cmd, coords = line.split()
        x,y,z=coords.split(",")
        x = [int(n) for n in x.split("=")[1].split("..")]
        y = [int(n) for n in y.split("=")[1].split("..")]
        z = [int(n) for n in z.split("=")[1].split("..")]
        assert x[0] <= x[1]
        assert y[0] <= y[1]
        assert z[0] <= z[1]
        inputs.append((cmd, x, y, z, 0))
    cubes = []
    while inputs:
        cmd, (min_x, max_x), (min_y, max_y), (min_z, max_z), idx = inputs.pop(0)
        to_remove = []
        to_add = []
        for index, cube in enumerate(cubes[idx:], start=idx):
            if intersection(((min_x, max_x), (min_y, max_y), (min_z, max_z)), cube):
                # We have to generate several shapes out of the new cube.
                if cmd == "on":
                    new_shapes = get_shapes(cube, ((min_x, max_x), (min_y, max_y), (min_z, max_z)))
                    for x_range, y_range, z_range in reversed(new_shapes):
                        inputs.insert(0, ("on", x_range, y_range, z_range, index+1))
                    break
                elif cmd == "off":
                    new_shapes = get_shapes(((min_x, max_x), (min_y, max_y), (min_z, max_z)), cube)
                    for x_range, y_range, z_range in new_shapes:
                        to_add.append((x_range, y_range, z_range))
                    to_remove.append(cube)
        else:
            if cmd == "on": 
                cubes.append(((min_x, max_x), (min_y, max_y), (min_z, max_z)))
        for cube in to_remove:
            cubes.remove(cube)
        for cube in to_add:
            cubes.append(cube)
    pixels_on = get_pixels(cubes)
    init_count = count_init_area(cubes)
    return pixels_on, init_count

if self_test:
    assert not axis_intersection(10, 10, 11, 12)
    assert not axis_intersection(11, 12, 10, 10)
    assert axis_intersection(10, 11, 11, 12)
    assert  axis_intersection(10, 12, 5, 10)
    get_shapes(((-20, 26), (-36, 17), (-47, 7)), ((-22, 28), (-29, 23), (-38, 16)), test=True)
    get_shapes(((27, 33), (-21, 23), (-26, 28)), ((27, 28), (-29, 23), (-38, 16)), test=True)
    get_shapes(((-20, 7), (24, 46), (-50, -1)), ((-20, 23), (24, 26), (-21, 29)), test=True)
    get_shapes(((-48, -32), (26, 41), (-47, -37)), ((-46, -23), (-6, 46), (-50, -1)), test=True)
    get_shapes(((-15, -4), (-14, 5), (-24, -11)), ((-9, -4), (-11, 36), (-45, 2)), test=True)
    assert(part2(test) == (39,39))
    assert(part2(test2)[1] == 590784)
    assert(part2(test3) == (2758514936282235,474140))
print(part2(data)[0])

