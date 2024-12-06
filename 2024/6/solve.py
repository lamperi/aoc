import os.path

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def part1(data):
    area = {}
    for y,line in enumerate(data.splitlines()):
        for x,c in enumerate(line):
            area[(y,x)] = c
            if c == "^":
                start = (y,x)

    pos = start
    dir = (-1,0)
    
    visited = set()
    while True:
        visited.add(pos)
        next_pos = pos[0] + dir[0], pos[1] + dir[1]
        if area.get(next_pos, None) is None:
            break
        elif area.get(next_pos, None) == "#":
            dir = dir[1], -1 * dir[0]
            next_pos = pos[0] + dir[0], pos[1] + dir[1]
            assert area.get(next_pos, None) == "."
        pos = next_pos
    return len(visited)
        
test = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""
print(part1(test))
print(part1(data))

def part2(data):
    area = {}
    for y,line in enumerate(data.splitlines()):
        for x,c in enumerate(line):
            area[(y,x)] = c
            if c == "^":
                start = (y,x)

    pos = start
    dir = (-1,0)
    
    s = 0
    for k, v in area.items():
        if v != ".":
            continue
        if is_loop(area | {k: '#'}, pos, dir):
            s += 1
    return s

def is_loop(area, pos, dir):
    visited = set()
    while True:
        if (pos,dir) not in visited:
            visited.add((pos, dir))
        else:
            return True
        next_pos = pos[0] + dir[0], pos[1] + dir[1]
        if area.get(next_pos, None) is None:
            return False
        elif area.get(next_pos, None) == "#":
            dir = dir[1], -1 * dir[0]
            next_pos = pos[0] + dir[0], pos[1] + dir[1]
            if area.get(next_pos, None) == "#":
                dir = dir[1], -1 * dir[0]
                next_pos = pos[0] + dir[0], pos[1] + dir[1]
                assert area.get(next_pos, None) == "."
        pos = next_pos

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))