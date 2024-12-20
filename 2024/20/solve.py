import os.path
from collections import deque

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def make_path(parents, init_state, end_state):
    path = [end_state]
    while path[-1] != init_state:
        path.append(parents[path[-1]])
    path.reverse()
    return path

def bfs(init_state, is_end, edges):
    queue = deque()
    queue.append((init_state, 0))
    parents = {init_state: None}
    while queue:
        node, path_len = queue.popleft()
        if is_end(node):
            return make_path(parents, init_state, node), parents

        for next_state in edges(node):
            if next_state not in parents:
                parents[next_state] = node
                queue.append((next_state, path_len + 1))
    return None, parents

def edges(pos, topology):
    for (dir) in (
        (-1, 0), (0, -1), (1, 0), (0, 1)
    ):
        next_pos = (pos[0] + dir[0], pos[1] + dir[1])
        is_free = topology.get(next_pos, "#") in "ES."
        if is_free:
            yield next_pos

def common(data, cheat_time):
    topology = {}
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            topology[(y,x)] = c
            if c == "S":
                start = (y,x)
            elif c == "E":
                end = (y,x)

    # This is the base case without cheating, build all nodes that can be
    # found without cheating.
    base_path, _ = bfs(start, lambda s: s == end, lambda pos: edges(pos, topology))
    base_time = len(base_path) - 1

    # Reachability - built time to reach each state from start.
    _, parents = bfs(start, lambda s: False, lambda pos: edges(pos, topology))
    time_from_start = {start: 0}
    for pos in parents.keys():
        path = make_path(parents, start, pos)
        time_from_start[pos] = len(path) - 1

    # Reachability - built time to end from each state reachable from end
    _, parents = bfs(end, lambda s: False, lambda pos: edges(pos, topology))
    time_until_end = {end: 0}
    for pos in parents.keys():
        path = make_path(parents, end, pos)
        time_until_end[pos] = len(path) - 1

    # This is an observation which makes this problem actually a bit easier.
    # There are no states reachable from start which are not in the best path
    # to the end, meaning there's unique path from start to end.
    # The solution below doesn't make use of this fact, but it tries to be correct.
    assert len(base_path) == len(time_from_start)

    # Need to find a save of 100 picoseconds. In tests, I'll try to find
    # a save of 50 picoseconds in part 2 and just cheats in part 1.
    require_save = 100 if len(topology) > 1000 else (50 if cheat_time > 2 else 1)

    # Find cheats that save (enough) time.
    # Iterate the original path, then checks all tiles reachable by cheating and
    # the time saved by reaching them.
    saves = 0
    for pos, time_to_reach_pos in time_from_start.items():
        for pos_diff in generate_reachable_diffs(cheat_time):
            next_pos = pos[0] + pos_diff[0], pos[1] + pos_diff[1]
            # Total time
            cheat_len = abs(pos_diff[0]) + abs(pos_diff[1])
            # Cheat can't end in a wall or outside of the area.
            # Checking if end is reachable from cheat end pos
            # is better.
            time_to_reach_end = time_until_end.get(next_pos, None)
            if time_to_reach_end is not None:
                path_time = time_to_reach_pos + cheat_len + time_to_reach_end
                time_save = base_time - path_time
                if time_save >= require_save:
                    saves += 1
    return saves

def generate_reachable_diffs(cheat_time):
    for x in range(0, cheat_time + 1):
        for y in range(0, cheat_time + 1 - x):
            if x == 0 and y == 0:
                continue
            yield (y, x)
            if (x != 0):
                yield (y, -x)
            if y != 0:
                yield (-y, x)
                if (x != 0):
                    yield (-y, -x)

def part1(data):
    return common(data, 2)

def part2(data):
    return common(data, 20)

test = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""
assert part1(test) == 44
print(part1(data))


# Override test for part 2.
# test = """ """

assert part2(test) == 285
print(part2(data))
