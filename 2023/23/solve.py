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

def solve(data, gen_adjacent):
    area = data.splitlines()
    pos = (0, 1)
    height = len(area)
    width = len(area[0])
    goal = height-1, width-2

    # preprocess the map.
    # find all the 
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
            if not (0 <= next_pos[0] < height):
                continue
            next_tile = area[next_pos[0]][next_pos[1]]
            if next_tile == "#":
                continue
            queue = [(next_pos, 1, v)]
            while queue:
                assert len(queue) == 1, queue
                pos, path_len, source = queue.pop()
                if pos in vertices:
                    edges[v].append((pos, path_len))
                    break
                tile = area[pos[0]][pos[1]]
                for adj in gen_adjacent(tile):
                    next_pos = pos[0] + adj[0], pos[1] + adj[1]
                    if next_pos == source:
                        continue
                    next_tile = area[next_pos[0]][next_pos[1]]
                    if next_tile == "#":
                        continue
                    queue.append((next_pos, path_len + 1, pos))

    max_len = 0
    pos = (0, 1)
    state = [(pos, 0, frozenset([pos]))]
    while state:
        pos, path_len, seen = state.pop()
        if pos == goal:
            max_len = max(path_len, max_len)
            continue
        for adj in edges[pos]:
            next_pos = adj[0]
            edge_len = adj[1]
            if next_pos in seen:
                continue
            next_seen = seen | frozenset([next_pos])
            state.append((next_pos, path_len + edge_len, next_seen))
    return max_len


def part1(data):
    return solve(data, adjacent)

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
    return solve(data, lambda _: ((1,0), (0,1), (-1,0), (0,-1)))

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))