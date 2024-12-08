from collections import defaultdict
import os.path

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def parse(data):
    antennas = defaultdict(list)
    for y, line in enumerate(data.splitlines()):
        max_y = y
        for x, c in enumerate(line):
            max_x = x
            if c != ".":
                antennas[c].append((y, x))
    return antennas, max_y, max_x

def part1(data):
    antennas, max_y, max_x = parse(data)
    
    antinodes = set()
    for _freq, coords in antennas.items():
        for c1 in coords:
            for c2 in coords:
                if c1 == c2:
                    continue
                dy = c1[0] - c2[0]
                dx = c1[1] - c2[1]
                antinode = c1[0] + dy, c1[1] + dx
                if 0 <= antinode[0] <= max_y and 0 <= antinode[1] <= max_x:
                    antinodes.add(antinode)
                antinode = c2[0] - dy, c2[1] - dx
                if 0 <= antinode[0] <= max_y and 0 <= antinode[1] <= max_x:
                    antinodes.add(antinode)
    return len(antinodes)

test = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""
print(part1(test))
print(part1(data))

def part2(data):
    antennas, max_y, max_x = parse(data)
    
    antinodes = set()
    for _freq, coords in antennas.items():
        for c1 in coords:
            for c2 in coords:
                if c1 == c2:
                    continue
                dy = c1[0] - c2[0]
                dx = c1[1] - c2[1] 
                antinode = c1
                while 0 <= antinode[0] <= max_y and 0 <= antinode[1] <= max_x:
                    antinodes.add(antinode)
                    antinode = antinode[0] + dy, antinode[1] + dx
                antinode = c2
                while 0 <= antinode[0] <= max_y and 0 <= antinode[1] <= max_x:
                    antinodes.add(antinode)
                    antinode = antinode[0] - dy, antinode[1] - dx
    return len(antinodes)

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))