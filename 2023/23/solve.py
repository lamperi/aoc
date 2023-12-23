import os.path

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def adjacent(tile):
    if tile == ".":
        return ((1,0), (0,1), (-1,0), (0,-1))
    elif tile == ">":
        return ((0,1), )
    elif tile == "<":
        return ((0,-1), )
    elif tile == "^":
        return ((-1,0), )
    elif tile == "v":
        return ((1,0), )
    else:
        assert False

def part1(data):
    area = data.splitlines()
    pos = (0, 1)
    goal = len(area)-2, len(area[-1])-2

    state = [(pos, 1, frozenset([pos]))]

    max_len = 0
    while state:
        pos, path_len, seen = state.pop()
        if pos == goal:
            if path_len > max_len:
                max_len = path_len
            continue

        tile = area[pos[0]][pos[1]]
        for adj in adjacent(tile):
            next_pos = pos[0] + adj[0], pos[1] + adj[1]
            
            next_tile = area[next_pos[0]][next_pos[1]]
            if next_tile == "#":
                continue
            if next_pos in seen:
                continue
            next_seen = seen | frozenset([next_pos])
            state.append((next_pos, path_len + 1, next_seen))
    return path_len

test = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""
print(part1(test))
print(part1(data))

def part2(data):
    area = data.splitlines()
    pos = (0, 1)
    goal = len(area)-1, len(area[-1])-2

    # preprocess
    vertices = set([pos, goal])
    for y, line in enumerate(area):
        for x, tile in enumerate(line):
            if (y,x) in vertices:
                continue
            if tile != "#":
                walls = 0
                for adj in ((1,0), (0,1), (-1,0), (0,-1)):
                    next_pos = y + adj[0], x + adj[1]
                    next_tile = area[next_pos[0]][next_pos[1]]
                    if next_tile == "#":
                        walls += 1
                if walls < 2:
                    vertices.add((y,x))

    edges = {v: [] for v in vertices}
    for v in vertices:
        for adj in ((1,0), (0,1), (-1,0), (0,-1)):
            next_pos = v[0] + adj[0], v[1] + adj[1]
            try:
                next_tile = area[next_pos[0]][next_pos[1]]
            except:
                next_tile = "#"
            if next_tile == "#":
                continue
            queue = [(next_pos, 1, frozenset([v, next_pos]))]
            r = 0
            while queue:
                r += 1
                assert len(queue) == 1, queue
                pos, path_len, seen = queue.pop()
                if pos in vertices:
                    edges[v].append((pos, path_len))
                    break
                for adj in ((1,0), (0,1), (-1,0), (0,-1)):
                    next_pos = pos[0] + adj[0], pos[1] + adj[1]
                    try:
                        next_tile = area[next_pos[0]][next_pos[1]]
                    except:
                        next_tile = "#"
                    if next_tile == "#":
                        continue
                    if next_pos in seen:
                        continue
                    next_seen = seen | frozenset([next_pos])
                    queue.append((next_pos, path_len + 1, next_seen))

    max_len = 0
    pos = (0, 1)
    state = [(pos, 0, frozenset([pos]))]
    while state:
        pos, path_len, seen = state.pop()
        if pos == goal:
            if path_len > max_len:
                max_len = path_len
            continue

        for adj in edges[pos]:
            next_pos = adj[0]
            edge_len = adj[1]
            if next_pos in seen:
                continue
            next_seen = seen | frozenset([next_pos])
            state.append((next_pos, path_len + edge_len, next_seen))
    return max_len

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))