import os.path
from functools import cache, cached_property

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()
INPUT = os.path.join(os.path.dirname(__file__), 'test_input.txt')
with open(INPUT) as f:
    test = f.read()

class Shape:
    def __init__(self, s):
        self.s = s
    
    @property
    def width(self):
        return len(self.s[0])

    @property
    def length(self):
        return len(self.s)

    @cached_property
    def tiles(self):
        coords = []
        for l, line in enumerate(self.s):
            for w, c in enumerate(line):
                if c == "#":
                    coords.append((w, l))
        return coords

    @cached_property
    def rotations_with_flips(self):
        variants = []
        seen = set([self.s])
        s = rotate(self.s)
        if s not in seen:
            variants.append(Shape(s))
            seen.add(s)
        s = rotate(s)
        if s not in seen:
            variants.append(Shape(s))
            seen.add(s)
        s = rotate(s)
        if s not in seen:
            variants.append(Shape(s))
            seen.add(s)
        s = flip(self.s)
        if s not in seen:
            variants.append(Shape(s))
            seen.add(s)
        s = rotate(s)
        if s not in seen:
            variants.append(Shape(s))
            seen.add(s)
        s = rotate(s)
        if s not in seen:
            variants.append(Shape(s))
            seen.add(s)
        s = rotate(s)
        if s not in seen:
            variants.append(Shape(s))
            seen.add(s)
        return variants

    def __repr__(self):
        return "\n".join(self.s)

def rotate(s):
    return tuple(''.join(reversed(a)) for a in zip(*s))

def flip(s):
    return tuple(''.join(reversed(a)) for a in s)

def part1(data):
    parts = data.split("\n\n")
    shapes = []
    for part in parts[:-1]:
        lines = part.splitlines()
        shapes.append(Shape(tuple(lines[1:])))

    regions = []
    for line in parts[-1].splitlines():
        size, presents = line.split(": ")
        width, length = size.split("x")
        width = int(width)
        length = int(length)
        presents = [int(p) for p in presents.split()]
        regions.append((width, length, presents))

    can_fit = 0
    i = 0
    for width, length, presents in regions:
        i += 1
        print(f"Solving problem #{i} for region size {width}x{length} with {sum(presents)} presents")
        if try_fit(width, length, presents, shapes):
            can_fit += 1
    return can_fit

def try_fit(width, length, presents, shapes):
    problem_shapes = []
    for i, p in enumerate(presents):
        for _ in range(0, p):
            problem_shapes.append(shapes[i])
    
    # Early reject: impossible puzzle
    space_taken = sum(len(s.tiles) for s in problem_shapes)
    area = [False] * (width*length)
    if space_taken > len(area):
        return False
    # Early accept: can fit without a hassle 
    trivial_fit = (width//3) * (length//3)
    if trivial_fit >= len(problem_shapes):
        return True

    return recurse(width, length, tuple(area), tuple(problem_shapes), True)

def shift(tile_gen, w, l):
    for i, j in tile_gen:
        yield i+w, j+l

@cache
def recurse(width, length, area, problem_shapes, first_shape):
    if len(problem_shapes) == 0:
        return True
    shape = problem_shapes[0]
    for w in range(0, width-shape.width+1):
        for l in range(0, length-shape.length+1):
            if all(area[j*width + i] == False for i,j in shift(shape.tiles, w, l)):
                new_area = list(area)
                for i,j in shift(shape.tiles, w, l):
                    new_area[j*width + i] = True
                if recurse(width, length, tuple(new_area), problem_shapes[1:], False):
                    return True
            if not first_shape:
                for shape_variant in shape.rotations_with_flips:
                    if all(area[j*width + i] == False for i,j in shift(shape_variant.tiles, w, l)):
                        new_area = list(area)
                        for i,j in shift(shape_variant.tiles, w, l):
                            new_area[j*width + i] = True
                        if recurse(width, length, tuple(new_area), problem_shapes[1:], False):
                            return True
    return False

print(part1(test))
print(part1(data))

def part2(data):
    return

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))