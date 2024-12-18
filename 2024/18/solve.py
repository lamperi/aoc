import os.path
import collections
import bisect

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def parse(data):
    coords = []
    for line in data.splitlines():
        x,y = line.split(",")
        y = int(y)
        x = int(x)
        coords.append((y,x))
    if len(coords) < 30:
        max_yx = 6 # inclusive
        first_n = 12
    else:
        max_yx = 70 # inclusive
        first_n = 1024
    return coords, max_yx, first_n

def make_edges_func(corrupted, max_yx):
    def edges(pos):
        for dir in (
            (1,0), (0, 1), (-1, 0), (0, -1)
        ):
            next_pos = pos[0] + dir[0], pos[1] + dir[1]
            if next_pos in corrupted:
                continue
            if 0 <= next_pos[0] <= max_yx and 0 <= next_pos[1] <= max_yx:
                yield next_pos
    return edges

def bfs(start, end, edges):
    deque = collections.deque([(0, start)])
    visited = set([(start)])
    while deque:
        steps, pos = deque.popleft()
        if pos == end:
            return steps
        for next_pos in edges(pos):
            if next_pos not in visited:
                visited.add(next_pos)
                deque.append((steps+1, next_pos))

def part1(data):
    coords, max_yx, first_n = parse(data)
        
    start = (0,0)
    end = (max_yx, max_yx)
    
    corrupted = set()
    for coord in coords[:first_n]:
        corrupted.add(coord)
    
    return bfs(start, end, make_edges_func(corrupted, max_yx))

def part2(data):
    coords, max_yx, first_n = parse(data)
        
    start = (0,0)
    end = (max_yx, max_yx)

    # Misuse Python's bisect key func.
    def bisect_key(index):
        corrupted = set()
        for coord in coords[:index+1]:
            corrupted.add(coord)
        r = bfs(start, end, make_edges_func(corrupted, max_yx))
        return 1 if r is None else -1

    idx = first_n + bisect.bisect_left(list(range(first_n, len(coords))), 0, key=bisect_key)
    y,x = coords[idx]
    return f"{x},{y}"

test = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""
assert part1(test) == 22
print(part1(data))

# Override test for part 2.
# test = """ """

print(part2(test))
assert part2(test) == "6,1"
print(part2(data))