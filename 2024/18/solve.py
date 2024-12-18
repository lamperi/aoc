import os.path
import heapq

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def part1(data):
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
        
    start = (0,0)
    end = (max_yx, max_yx)
    
    corrupted = set()
    for coord in coords[:first_n]:
        corrupted.add(coord)
    
    heap = [(0, start)]
    visited = set([(start)])
    while heap:
        steps, pos = heapq.heappop(heap)
        if pos == end:
            return steps
        for dir in (
            (1,0), (0, 1), (-1, 0), (0, -1)
        ):
            next_pos = pos[0] + dir[0], pos[1] + dir[1]
            if next_pos in corrupted:
                continue
            if 0 <= next_pos[0] <= max_yx and 0 <= next_pos[1] <= max_yx:
                if next_pos not in visited:
                    visited.add(next_pos)
                    heapq.heappush(heap, (steps+1, next_pos))
    
    return

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
print(part1(test))
print(part1(data))

def part2(data):
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
        
    start = (0,0)
    end = (max_yx, max_yx)
    
    for attempt in range(first_n, len(coords)):
        found = False
        
        corrupted = set()
        for coord in coords[:attempt+1]:
            corrupted.add(coord)
        
        heap = [(0, start)]
        visited = set([(start)])
        while heap:
            steps, pos = heapq.heappop(heap)
            if pos == end:
                found = True
                break
            for dir in (
                (1,0), (0, 1), (-1, 0), (0, -1)
            ):
                next_pos = pos[0] + dir[0], pos[1] + dir[1]
                if next_pos in corrupted:
                    continue
                if 0 <= next_pos[0] <= max_yx and 0 <= next_pos[1] <= max_yx:
                    if next_pos not in visited:
                        visited.add(next_pos)
                        heapq.heappush(heap, (steps+1, next_pos))
        if not found:
            y,x = coords[attempt]
            return f"{x},{y}"

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))