import os.path
import bisect

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def part1(data):
    universe = data.splitlines()

    # expand the universe
    new_universe = []
    for line in universe:
        if all(c == "." for c in line):
            new_universe.append(line)
        new_universe.append(line)
    universe = new_universe

    new_universe = [[] for _ in universe]
    for i, _ in enumerate(universe[0]):
        is_empty_i = all(line[i] == "." for line in universe)
        for j, line in enumerate(universe):
            if is_empty_i:
                new_universe[j].append(".")
            new_universe[j].append(line[i])
    universe = new_universe
    
    #print("\n".join("".join(c for c in line) for line in galaxy))
    
    galaxies = []
    for y, line in enumerate(universe):
        for x, c in enumerate(line):
            if c == "#":
                galaxies.append((y,x))

    s = 0   
    for i, a in enumerate(galaxies):
        for b in galaxies[i+1:]:
            yd = abs(b[0] - a[0])
            xd = abs(b[1] - a[1])
            s += yd + xd
    return s

test = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""
print(part1(test), "==", 374)
print(part1(data))

def part2(data, expand_factor=1000000):
    universe = data.splitlines()

    # mark the expansion points
    empty_y_space = []
    empty_x_space = []

    for y, line in enumerate(universe):
        if all(c == "." for c in line):
            empty_y_space.append(y)

    for i, _ in enumerate(universe[0]):
        if all(line[i] == "." for line in universe):
            empty_x_space.append(i)

    # Find galaxies
    galaxies = []
    for y, line in enumerate(universe):
        for x, c in enumerate(line):
            if c == "#":
                galaxies.append((y,x))

    # Count the sum of distances between galaxies
    s = 0   
    for i, a in enumerate(galaxies):
        for b in galaxies[i+1:]:
            max_y = max(b[0], a[0])
            min_y = min(b[0], a[0])
            max_x = max(b[1], a[1])
            min_x = min(b[1], a[1])

            a1 = bisect.bisect(empty_y_space, min_y)
            a2 = bisect.bisect(empty_y_space, max_y)
            y_empty = a2 - a1

            a1 = bisect.bisect(empty_x_space, min_x)
            a2 = bisect.bisect(empty_x_space, max_x)
            x_empty = a2 - a1

            yd = max_y - min_y + y_empty*(expand_factor-1)
            xd = max_x - min_x + x_empty*(expand_factor-1)
            s += yd + xd
    return s


# Override test for part 2.
# test = """ """

print(part2(test, expand_factor=10), "==", 1030)
print(part2(test, expand_factor=100), "==", 8410)
print(part2(data))