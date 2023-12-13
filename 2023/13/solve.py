import os.path

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()


def vertical_line(mirror, x):
    return "".join(m[x] for m in mirror)


def horizontal_line(mirror, y):
    return mirror[y]

def distance(s1, s2):
    return sum(0 if a1 == a2 else 1 for a1, a2 in zip(s1, s2))

def find_line(mirror, length, line_getter, expected_cracks):
    found = None
    for z in range(length-1):
        z0 = z
        z1 = z+1
        total_d = 0
        while z0 >= 0 and z1 < length:
            total_d += distance(line_getter(mirror, z0), line_getter(mirror, z1))
            if total_d > expected_cracks:
                break
            z0 -= 1
            z1 += 1
        if total_d == expected_cracks:
            found = z
    return found

def generic(data, expected_cracks):
    mirrors = data.split("\n\n")

    s = 0
    for mirror in mirrors:
        mirror = mirror.splitlines()

        found_y = find_line(mirror, len(mirror), horizontal_line, expected_cracks)
        found_x = find_line(mirror, len(mirror[0]), vertical_line, expected_cracks)

        if found_x is not None:
            s += found_x +1 
        elif found_y is not None:
            s += 100*(found_y +1)
    return s

def part1(data):
    return generic(data, 0)

test = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""
print(part1(test))
print(part1(data))


def part2(data):
    return generic(data, 1)

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))