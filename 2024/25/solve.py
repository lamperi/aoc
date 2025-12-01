import os.path

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def part1(data):
    schematics = data.split("\n\n")
    locks = []
    keys = []

    for schematic in schematics:        
        item = []
        schematic = schematic.splitlines()
        for x in range(5):
            max_y = 0
            for y in range(6):
                if schematic[y][x] == schematic[0][0]:
                    max_y = y
            item.append(max_y)

        if schematic[0][0] == "#":
            locks.append(item)
        else:
            key = [(5 - y) for y in item]
            keys.append(key)

    fitting = 0
    for lock in locks:
        for key in keys:
            if all(x+y < 6 for x,y in zip(lock,key)):
                fitting += 1

    return fitting

test = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""
assert part1(test) == 3
print(part1(data))
