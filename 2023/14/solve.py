import os.path

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def part1(data):
    lines = data.splitlines()
    rocks = set()
    walls = set()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "O":
                rocks.add((y,x))
            elif c == "#":
                walls.add((y,x))
    
    changed = True
    while changed:
        changed = False
        for rock in list(sorted(rocks)):
            y, x = rock
            north = y-1, x
            if y > 0 and north not in walls and north not in rocks:
                rocks.add(north)
                rocks.remove(rock)
                changed = True
    
    s = 0
    for y, _ in rocks:
        s += len(lines) - y
    return s

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

def tilt(rocks, walls, dir, limits):
    changed = True
    while changed:
        changed = False
        for rock in list(sorted(rocks)):
            y, x = rock
            yn = y+dir[0]
            xn = x+dir[1]
            
            if 0 <= yn < limits[0] and 0 <= xn < limits[1]:
                north = yn, xn
                if north not in walls and north not in rocks:
                    rocks.add(north)
                    rocks.remove(rock)
                    changed = True

def part2(data):
    lines = data.splitlines()
    rocks = set()
    walls = set()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "O":
                rocks.add((y,x))
            elif c == "#":
                walls.add((y,x))
    
    limits = (len(lines), len(lines[0]))
    states = {frozenset(rocks): 0}
    total_load = sum(limits[0] - y for y, _ in rocks)
    loads = [total_load]
    goal = 1000000000
    for iteration in range(1, goal):
        tilt(rocks, walls, (-1,  0), limits)
        tilt(rocks, walls, ( 0, -1), limits)
        tilt(rocks, walls, ( 1,  0), limits)
        tilt(rocks, walls, ( 0,  1), limits)
        total_load = sum(limits[0] - y for y, _ in rocks)
        loads.append(total_load)
    
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