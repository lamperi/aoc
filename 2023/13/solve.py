import os.path

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def vertical_line(mirror, x):
    return "".join(m[x] for m in mirror)

def part1(data):
    mirrors = data.split("\n\n")

    s = 0
    for mirror in mirrors:
        mirror = mirror.splitlines()

        # horizontal
        found_y = None
        for y, _ in enumerate(mirror):
            y0 = y
            y1 = y+1
            perfect = False
            while y0 >= 0 and y1 < len(mirror):
                if mirror[y0] == mirror[y1]:
                    perfect = True
                else:
                    perfect = False
                    break
                y0 -= 1
                y1 += 1
            if perfect:
                assert found_y is None
                found_y = y

        # vertical
        found_x = None
        for x, _ in enumerate(mirror[0]):
            x0 = x
            x1 = x+1
            perfect = False
            while x0 >= 0 and x1 < len(mirror[0]):
                if vertical_line(mirror, x0) == vertical_line(mirror, x1):
                    perfect = True
                else:
                    perfect = False
                    break
                x0 -= 1
                x1 += 1
            if perfect:
                assert found_x is None
                found_x = x

        assert found_x is None or found_y is None
        assert found_x is not None or found_y is not None
        if found_x is not None:
            s += found_x +1 
        elif found_y is not None:
            s += 100*(found_y +1)
    return s

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

def distance(s1, s2):
    return sum(0 if a1 == a2 else 1 for a1, a2 in zip(s1, s2))

def part2(data):
    mirrors = data.split("\n\n")

    s = 0
    for mirror in mirrors:
        mirror = mirror.splitlines()

        # horizontal
        found_y = None
        for y, _ in enumerate(mirror):
            y0 = y
            y1 = y+1
            perfect = False
            total_d = 0
            while y0 >= 0 and y1 < len(mirror):
                d = distance(mirror[y0], mirror[y1])
                total_d += d
                if d in (0, 1):
                    perfect = True
                else:
                    perfect = False
                    break
                y0 -= 1
                y1 += 1
            if perfect and total_d == 1:
                assert found_y is None
                found_y = y

        # vertical
        found_x = None
        for x, _ in enumerate(mirror[0]):
            x0 = x
            x1 = x+1
            perfect = False
            total_d = 0
            while x0 >= 0 and x1 < len(mirror[0]):
                d = distance(vertical_line(mirror, x0), vertical_line(mirror, x1))
                total_d += d
                if d in (0, 1):
                    perfect = True
                else:
                    perfect = False
                    break
                x0 -= 1
                x1 += 1
            if perfect and total_d == 1:
                assert found_x is None
                found_x = x

        assert found_x is None or found_y is None
        assert found_x is not None or found_y is not None
        if found_x is not None:
            s += found_x +1 
        elif found_y is not None:
            s += 100*(found_y +1)
    return s

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))