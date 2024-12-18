import os.path
import heapq
import dataclasses

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

@dataclasses.dataclass
class Node:
    cost: int
    state: any
    previous: 'Node'

    def path(self):
        path = [self.state]
        node = self
        while node.previous is not None:
            node = node.previous
            path.append(node.state)
        return path

    def __repr__(self):
        return f'Node value: {self.state}, cost: {self.cost}'

    def __lt__(self, other):
        return self.cost < other.cost

def dijkstra(init_state, is_end, edges):
    queue = []
    visited_states = {}
    visited_states[init_state] = 0
    heapq.heappush(queue, Node(0, init_state, None))
    while queue:
        node = heapq.heappop(queue)
        if is_end(node.state):
            return node

        for (next_state, cost) in edges(node.state):
            next_cost = node.cost + cost
            if next_cost < visited_states.get(next_state, next_cost+1):
                visited_states[next_state] = next_cost
                heapq.heappush(queue, Node(next_cost, next_state, node))

def dijkstra_all(init_state, is_end, edges):
    queue = []
    visited_states = {}
    visited_states[init_state] = 0
    heapq.heappush(queue, Node(0, init_state, None))
    best_complete = float('inf')
    paths = []
    while queue:
        node = heapq.heappop(queue)
        if is_end(node.state):
            if node.cost < best_complete:
                best_complete = node.cost
                paths.clear()
            paths.append(node)
        if node.cost > best_complete:
            continue

        for (next_state, cost) in edges(node.state):
            next_cost = node.cost + cost
            if next_cost <= visited_states.get(next_state, next_cost+1):
                visited_states[next_state] = next_cost
                heapq.heappush(queue, Node(next_cost, next_state, node))
    return paths

def part1(data):
    topology = {}
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            topology[(y,x)] = c
            if c == "S":
                start = (y,x)
            elif c == "E":
                end = (y,x)
    def is_end(state):
        pos, _ = state
        return pos == end
    def edges(state):
        pos, dir = state
        for (next_pos, next_dir, cost) in (
            ((pos[0] + dir[0], pos[1] + dir[1]), dir, 1),
            (pos, (dir[1] * -1, dir[0]), 1000),
            (pos, (dir[1], dir[0] * -1), 1000)
        ):
            if topology.get(next_pos) in "ES.":
                yield (next_pos, next_dir), cost

    node = dijkstra((start, (0, 1)), is_end, edges)
    return node.cost

def part2(data):
    topology = {}
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            topology[(y,x)] = c
            if c == "S":
                start = (y,x)
            elif c == "E":
                end = (y,x)

    def is_end(state):
        pos, _ = state
        return pos == end
    def edges(state):
        pos, dir = state
        for (next_pos, next_dir, cost) in (
            ((pos[0] + dir[0], pos[1] + dir[1]), dir, 1),
            (pos, (dir[1] * -1, dir[0]), 1000),
            (pos, (dir[1], dir[0] * -1), 1000)
        ):
            if topology.get(next_pos) in "ES.":
                yield (next_pos, next_dir), cost

    nodes = dijkstra_all((start, (0, 1)), is_end, edges)
    visited_tiles = set()
    for node in nodes:
        visited_tiles.update(
                (pos for (pos, _dir) in node.path())
        )
    return len(visited_tiles)

test = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""
test2 = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""
test3 ="""####################
####.##########.####
##..............####
##.#.##.#######.####
#..#.##.....#...#..#
##.#.######.#.#.#.##
##....#...........E#
##.####.#####.###.##
#.........###.#...##
##.####.#.###.#.####
#S.#################
####################"""

assert part1(test) == 7036
assert part1(test2) == 11048
assert part1(test3) == 4021
print(part1(data))

assert part2(test) == 45
assert part2(test2) == 64
assert part2(test3) == 22
print(part2(data))