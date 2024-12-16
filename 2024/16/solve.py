import os.path
import heapq

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def part1(data):
    topology = {}
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            topology[(y,x)] = c
            if c == "S":
                start = (y,x)
            elif c == "E":
                end = (y,x)
    
    queue = []
    dir = (0, 1)
    visited_states = {}
    visited_states[(start, dir)] = 0
    heapq.heappush(queue, (0, start, dir))
    while queue:
        points, pos, dir = heapq.heappop(queue)
        
        if pos == end:
            return points
        
        for (next_pos, next_dir, cost) in (
            ((pos[0] + dir[0], pos[1] + dir[1]), dir, 1),
            (pos, (dir[1] * -1, dir[0]), 1000),
            (pos, (dir[1], dir[0] * -1), 1000)
        ):
            next_points = points + cost
            if topology.get(next_pos) in "ES.":
                if next_points < visited_states.get((next_pos, next_dir), next_points+1):
                    visited_states[(next_pos, next_dir)] = next_points
                    heapq.heappush(queue, (next_points, next_pos, next_dir))

    return -1



def update_best_path(best_path, current_key, prev_key, next_points):
    if current_key in best_path:
        current_best_points, current_path = best_path[current_key]
        if current_best_points == next_points:
            _, prev_path = best_path[prev_key]
            # There are multiple ways to a state.
            current_path.update(prev_path)
        elif current_best_points > next_points:
            _, prev_path = best_path[prev_key]
            best_path[current_key] = (next_points, prev_path | set([current_key[0]]))
    else:
        _, prev_path = best_path[prev_key]
        best_path[current_key] = (next_points, prev_path | set([current_key[0]]))

def part2(data):
    topology = {}
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            topology[(y,x)] = c
            if c == "S":
                start = (y,x)
            elif c == "E":
                end = (y,x)
    
    queue = []
    dir = (0, 1)
    visited_states = {}
    visited_states[(start, dir)] = 0
    heapq.heappush(queue, (0, start, dir))
    best_path = {(start, dir): (0, set([start]))}
    best_complete = None
    while queue:
        points, pos, dir = heapq.heappop(queue)
        # Prune paths that can never be optimal.
        if best_complete and points > best_complete:
            continue
        if pos == end:
            if best_complete is None or points < best_complete:
                best_complete = points
            continue
        
        for (next_pos, next_dir, cost) in (
            ((pos[0] + dir[0], pos[1] + dir[1]), dir, 1),
            (pos, (dir[1] * -1, dir[0]), 1000),
            (pos, (dir[1], dir[0] * -1), 1000)
        ):
            next_points = points + cost
            if topology.get(next_pos) in "ES.":
                update_best_path(best_path, (next_pos, next_dir), (pos, dir), next_points)
                if next_points < visited_states.get((next_pos, next_dir), next_points+1):
                    visited_states[(next_pos, next_dir)] = next_points
                    heapq.heappush(queue, (next_points, next_pos, next_dir))

    min_points_for_end = None
    all_tiles = set()
    for (pos, dir), (points, tiles) in best_path.items():
        if pos == end:
            if min_points_for_end is None or min_points_for_end > points:
                min_points_for_end = points
                all_tiles.clear()
                all_tiles.update(tiles)
            elif min_points_for_end == points:
                all_tiles.update(tiles)
    return len(all_tiles)

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