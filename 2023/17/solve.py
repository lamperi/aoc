import os.path
import heapq
import copy

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def debug_print(data, path, debug=False):
    if not debug:
        return
    s = ""
    di = {k: v for k,v in path}
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            c = di.get((y,x), c)
            if c == (0,1):
                c = ">"
            elif c == (0,-1):
                c = "<"
            elif c == (-1,0):
                c = "^"
            elif c == (1,0):
                c = "v"
            else:
                c = " "
            s += c
        s += "\n"
    print(s)
    #print(path)

def generic_solve(data, min_straight, max_straight, debug=False):
    area = {}
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            area[(y,x)] = int(c)
    goal = (y, x)

    heat = 0
    pos = (0, 0)
    dir = (0, 0)
    straight = 0
    path = []
    states = [(heat, pos, dir, straight, path)]

    visited = set()
    while states:
        heat, pos, dir, straight, path = heapq.heappop(states)
        if (pos, dir, straight) in visited:
            continue
        visited.add((pos, dir, straight))
        if pos == goal:
            debug_print(data, path, debug)
            return heat
        for d in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            same_dir = d == dir
            if same_dir and straight >= max_straight:
                continue
            opposite_dir = d == (-dir[0], -dir[1])
            if opposite_dir:
                continue
            new_pos = pos[0] + d[0], pos[1] + d[1]
            new_pos_heat = area.get(new_pos, None)
            if new_pos_heat is None:
                continue
            new_path = [(new_pos, d)]
            if same_dir:
                new_straight = straight + 1
            else:
                new_straight = 1
                while new_straight < min_straight:
                    new_pos = new_pos[0] + d[0], new_pos[1] + d[1]
                    new_pos_heat += area.get(new_pos, 0)
                    new_straight += 1
                    new_path.append((new_pos, d))
                if new_pos not in area.keys():
                    continue
            if debug:
                # incurs a lot of copying, only run this path if debug is requested.
                new_path = path + new_path
            else:
                new_path = None
            item = (heat + new_pos_heat, new_pos, d, new_straight, new_path)
            heapq.heappush(states, item)

def part1(data, debug=False):
    return generic_solve(data, 1, 3, debug)

test = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""
print("test 1", t1 := part1(test))
assert t1 == 102
print(part1(data))

def part2(data, debug=False):
    return generic_solve(data, 4, 10, debug)

print("test 2.1", t21 := part2(test))
assert(t21 == 94)

# Override test for part 2.
test = """111111111111
999999999991
999999999991
999999999991
999999999991"""

print("test 2.2", t22 := part2(test))
assert(t22 == 71)

print(part2(data))
