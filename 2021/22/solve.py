import os.path
from itertools import combinations
from collections import deque
import sys
self_test = '--self-test' in sys.argv

with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as f:
    data = f.read()

with open(os.path.join(os.path.dirname(__file__), 'test1.txt')) as f:
    test = f.read()

with open(os.path.join(os.path.dirname(__file__), 'test2.txt')) as f:
    test2 = f.read()

with open(os.path.join(os.path.dirname(__file__), 'test3.txt')) as f:
    test3 = f.read()


def part1(data):
    inputs = []
    for line in data.splitlines():
        cmd, coords = line.split()
        x, y, z = coords.split(',')
        x = [int(n) for n in x.split('=')[1].split('..')]
        y = [int(n) for n in y.split('=')[1].split('..')]
        z = [int(n) for n in z.split('=')[1].split('..')]
        inputs.append((cmd, x, y, z))
    on = set()
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
                    if cmd == 'on':
                        on.add((x, y, z))
                    elif cmd == 'off' and (x, y, z) in on:
                        on.remove((x, y, z))
    return len(on)


if self_test:
    assert(part1(test) == 39)
    assert(part1(test2) == 590784)
print(part1(data))


def axis_intersection(min_x, max_x, min_x2, max_x2):
    return ((max_x >= min_x2 and min_x <= min_x2)
            or max_x2 >= min_x and min_x2 <= min_x)


def intersection(rectangle1, rectangle2):
    (min_x, max_x), (min_y, max_y), (min_z, max_z) = rectangle1
    (min_x2, max_x2), (min_y2, max_y2), (min_z2, max_z2) = rectangle2
    return (axis_intersection(min_x, max_x, min_x2, max_x2)
            and axis_intersection(min_y, max_y, min_y2, max_y2)
            and axis_intersection(min_z, max_z, min_z2, max_z2))


def handle_axis(rectangle1, rectangle2, ax):
    shapes = []
    min_a1, max_a1 = rectangle1[ax]
    min_a2, max_a2 = rectangle2[ax]
    # case 1: cut the part where max_a2 > max_a1
    if max_a1 < max_a2:
        shapes.append(rectangle2[:ax] + ((max_a1+1, max_a2),) + rectangle2[ax+1:])
        max_a2 = max_a1
    # case 2: cut the part where min_a2 < min_a1
    if min_a2 < min_a1:
        shapes.append(rectangle2[:ax] + ((min_a2, min_a1-1),) + rectangle2[ax+1:])
        min_a2 = min_a1
    # update the axis range so we can use it for next axis
    return rectangle2[:ax] + ((min_a2, max_a2),) + rectangle2[ax+1:], shapes


def divide_rectangle_into_non_intersecting_shapes(rectangle1, rectangle2):
    shapes = []
    rectangle2, s = handle_axis(rectangle1, rectangle2, 0)
    shapes.extend(s)
    rectangle2, s = handle_axis(rectangle1, rectangle2, 1)
    shapes.extend(s)
    _, s = handle_axis(rectangle1, rectangle2, 2)
    shapes.extend(s)
    return shapes


def get_pixels(rectangles):
    pixels_on = 0
    for (min_x, max_x), (min_y, max_y), (min_z, max_z) in rectangles:
        pixels_on += abs(1 + max_x - min_x) * \
            abs(1 + max_y - min_y) * abs(1 + max_z - min_z)
    return pixels_on


def get_init_area(rectangles):
    on = set()
    for (min_x, max_x), (min_y, max_y), (min_z, max_z) in rectangles:
        min_x = max(-50, min_x)
        max_x = min(50, max_x)
        min_y = max(-50, min_y)
        max_y = min(50, max_y)
        min_z = max(-50, min_z)
        max_z = min(50, max_z)
        for x in range(min_x, max_x+1):
            for y in range(min_y, max_y+1):
                for z in range(min_z, max_z+1):
                    on.add((x, y, z))
    return on


def count_init_area(rectangles):
    return len(get_init_area(rectangles))


def part2(data):
    inputs = deque()
    for line in data.splitlines():
        cmd, coords = line.split()
        x, y, z = coords.split(',')
        x = [int(n) for n in x.split('=')[1].split('..')]
        y = [int(n) for n in y.split('=')[1].split('..')]
        z = [int(n) for n in z.split('=')[1].split('..')]
        assert x[0] <= x[1]
        assert y[0] <= y[1]
        assert z[0] <= z[1]
        inputs.append((cmd, (x, y, z), 0))
    non_intersecting_shapes = []
    while inputs:
        cmd, current, idx = inputs.popleft()
        to_remove = []
        to_add = []
        for index, shape in enumerate(non_intersecting_shapes[idx:], start=idx):
            if intersection(current, shape):
                if cmd == 'on':
                    new_shapes = divide_rectangle_into_non_intersecting_shapes(
                        shape, current)
                    # Get shapes that don't intersect with this rectangle.
                    # Push into beginning of inputs because order matters.
                    # Save index so we don't check already visited rectangles again (Expensive)
                    next_inputs = [('on', rectangle, index+1)
                                   for rectangle in new_shapes]
                    inputs.extendleft(next_inputs)
                    break
                elif cmd == 'off':
                    new_shapes = divide_rectangle_into_non_intersecting_shapes(
                        current, shape)
                    to_add.extend(new_shapes)
                    to_remove.append(shape)
        else:
            # Only add the rectangle if we didn't have to split it.
            # With break
            if cmd == 'on':
                non_intersecting_shapes.append(current)
                continue
            # Add all pieces that are left when
            for shape in to_remove:
                non_intersecting_shapes.remove(shape)
            for shape in to_add:
                non_intersecting_shapes.append(shape)
    pixels_on = get_pixels(non_intersecting_shapes)
    init_count = count_init_area(non_intersecting_shapes)
    return pixels_on, init_count


if self_test:
    assert(part2(test) == (39, 39))
    assert(part2(test2)[1] == 590784)
    assert(part2(test3) == (2758514936282235, 474140))
print(part2(data)[0])
