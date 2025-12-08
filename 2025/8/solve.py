import os.path
from collections import Counter

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()
INPUT = os.path.join(os.path.dirname(__file__), 'test_input.txt')
with open(INPUT) as f:
    test = f.read()

def dist_square(b1, b2):
    x1,y1,z1 = b1
    x2,y2,z2 = b2
    return (x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2

def parse(data):
    boxes = []
    for line in data.splitlines():
        x,y,z = [int(i) for i in line.split(",")]
        boxes.append((x,y,z))
        
    distances = []
    for i, b1 in enumerate(boxes):
        for j, b2 in enumerate(boxes[i+1:], start=i+1):
            d = dist_square(b1, b2)
            distances.append((d, i, j))
    distances.sort()
    return boxes, distances

def run_loop(distances, max_groups=None) -> dict[int, int] | tuple[int, int]:
    junction = {}
    junction_id = 1
    connected = 0
    for _, i, j in distances:
        if i not in junction and j not in junction:
            junction[i] = junction_id
            junction[j] = junction_id
            junction_id += 1
            connected += 2
        elif i in junction and j not in junction:
            junction[j] = junction[i]
            connected += 1
        elif i not in junction and j in junction:
            junction[i] = junction[j]
            connected += 1
        else:
            key = junction[i]
            not_key = junction[j]
            junction = {k: v if v != not_key else key for k, v in junction.items()}
        if connected == max_groups:
            return i, j

    return junction

def part1(data):
    boxes, distances = parse(data)
    
    r = 1000 if len(boxes) > 20 else 10
    
    junction = run_loop(distances[:r])
    
    v = Counter(junction.values())
    a,b,c = [b for _, b in v.most_common(3)]
    return a * b * c


print(part1(test))
print(part1(data))

def part2(data):
    boxes, distances = parse(data)
        
    i, j = run_loop(distances, len(boxes))
    return boxes[i][0]*boxes[j][0]

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))