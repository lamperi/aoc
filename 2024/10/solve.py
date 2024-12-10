import os.path
import collections

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def common(data):
    starts = []
    area = {}
    for y,line in enumerate(data.splitlines()):
        for x,c in enumerate(line):
            area[(y,x)] = int(c)
            if c == "0":
                start = (y,x)
                starts.append(start)
                
    peaks_reachable = 0
    unique_paths = 0
    for start in starts:
        queue = collections.deque([(start, 0)])
        trails = set()
        trails_c = 0
        while queue:
            pos, n = queue.popleft()
            for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
                new_pos = pos[0] + dy, pos[1] + dx
                if area.get(new_pos, -1) == n+1:
                    if n+1 == 9:
                        trails.add(new_pos)
                        trails_c += 1
                    else:
                        queue.append((new_pos, n+1))
        peaks_reachable += len(trails)
        unique_paths += trails_c
    return peaks_reachable, unique_paths

def part1(data):
    peaks_reachable, _ = common(data)
    return peaks_reachable

test = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""
print(part1(test))
print(part1(data))

def part2(data):
    _, unique_paths = common(data)
    return unique_paths

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))