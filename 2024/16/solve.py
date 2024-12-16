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
    visited_states = set()
    visited_states.add((start, dir))
    heapq.heappush(queue, (0, start, dir))
    while queue:
        points, pos, dir = heapq.heappop(queue)
        
        next_pos = pos[0] + dir[0], pos[1] + dir[1]
        if next_pos == end:
            return points + 1
        
        if topology.get(next_pos) == ".":
            if (next_pos, dir) not in visited_states:
                visited_states.add((next_pos, dir))
                heapq.heappush(queue, (points + 1, next_pos, dir))
        
        # (0,1) => (-1,0)
        next_dir = dir[1] * -1, dir[0]
        if (pos, next_dir) not in visited_states:
            visited_states.add((pos, next_dir))
            heapq.heappush(queue, (points + 1000, pos, next_dir))
        # (0,1) => (1,0)
        next_dir = dir[1], dir[0] * -1
        if (pos, next_dir) not in visited_states:
            visited_states.add((pos, next_dir))
            heapq.heappush(queue, (points + 1000, pos, next_dir))

    return -1

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
print(part1(test))
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
print(part1(test2))
print(part1(data))

def update_best_path(best_path, key, prev_key, next_points):
    if key in best_path:
        t = best_path[key]
        if t[0] == next_points:
            prev = best_path[prev_key]
            t[1].update(prev[1])
    else:
        prev = best_path[prev_key]
        best_path[key] = (next_points, prev[1] | set([key[0]]))

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
    visited_states = set()
    visited_states.add((start, dir))
    heapq.heappush(queue, (0, start, dir))
    best_path = {(start, dir): (0, set([start]))}
    while queue:
        points, pos, dir = heapq.heappop(queue)
        
        next_pos = pos[0] + dir[0], pos[1] + dir[1]
        update_best_path(best_path, (next_pos, dir), (pos, dir), points + 1)

        if next_pos == end:
            continue

        if topology.get(next_pos) == ".":
            if (next_pos, dir) not in visited_states:
                visited_states.add((next_pos, dir))
                heapq.heappush(queue, (points + 1, next_pos, dir))
        
        # (0,1) => (-1,0)
        next_dir = dir[1] * -1, dir[0]
        update_best_path(best_path, (pos, next_dir), (pos, dir), points + 1000)
        if (pos, next_dir) not in visited_states:
            visited_states.add((pos, next_dir))
            heapq.heappush(queue, (points + 1000, pos, next_dir))
        # (0,1) => (1,0)
        next_dir = dir[1], dir[0] * -1
        update_best_path(best_path, (pos, next_dir), (pos, dir), points + 1000)
        if (pos, next_dir) not in visited_states:
            visited_states.add((pos, next_dir))
            heapq.heappush(queue, (points + 1000, pos, next_dir))

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

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))