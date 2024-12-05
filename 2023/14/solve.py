import os.path

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def tilt(rocks, walls, dir, limits):
    (h, w) = limits

    def sort_key(rock):
        y, x = rock
        return -h*y*dir[0] -w*x*dir[1]

    for rock in list(sorted(rocks, key=sort_key)):
        y, x = ok_pos = rock
        while True:
            yn = y + dir[0]
            xn = x + dir[1]
            if 0 <= yn < h and 0 <= xn < w and (yn, xn) not in walls and (yn, xn) not in rocks:
                y, x = ok_pos = yn, xn
            else:
                break
        if ok_pos != rock:
            rocks.add(ok_pos)
            rocks.remove(rock)

def load(rocks, h):
    return sum(h - y for y, _ in rocks)

def parse(data):
    lines = data.splitlines()
    rocks = set()
    walls = set()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "O":
                rocks.add((y,x))
            elif c == "#":
                walls.add((y,x))
    return (len(lines), len(lines[0])), rocks, frozenset(walls)

def part1(data):
    (h, w), rocks, walls = parse(data)
    tilt(rocks, walls, (-1,  0), (h, w))
    return load(rocks, h)

test = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""
print(part1(test))
print(part1(data))



def part2(data):
    limits, rocks, walls = parse(data)
    (h, w) = limits
    states = {frozenset(rocks): 0}
    loads = [load(rocks, h)]
    goal = 1000000000
    for iteration in range(1, goal):
        tilt(rocks, walls, (-1,  0), limits)
        tilt(rocks, walls, ( 0, -1), limits)
        tilt(rocks, walls, ( 1,  0), limits)
        tilt(rocks, walls, ( 0,  1), limits)
        loads.append(load(rocks, h))
    
        st = frozenset(rocks)
        if st in states:
            cur = iteration
            prev = states[st]
            cycle_len = cur - prev
            left = goal - cur
            mod = left % cycle_len
            idx_of_solution = prev + mod
            #print(f"encountered state at {prev} and again at {cur}")
            #print(f"mod should be {mod} at {goal}")
            #print(f"index should be {idx_of_solution} of {loads}")
            return loads[idx_of_solution]
        else:
            states[st] = iteration

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))

