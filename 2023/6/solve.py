import os.path
import math

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def part1(data):
    time, distance, *_ = data.splitlines()
    time = [int(x) for x in time.split()[1:]]
    distance = [int(x) for x in distance.split()[1:]]
    
    s = []
    for t, d in zip(time, distance):
        y = 0
        for hold in range(t):
            dist = (t-hold)*hold
            if dist > d:
                y += 1
        s.append(y)
    return math.prod(s)

test = """Time:      7  15   30
Distance:  9  40  200"""
print(part1(test))
print(part1(data))

def part2(data):
    time, distance, *_ = data.splitlines()
    time = int("".join([x for x in time.split()[1:]]))
    distance = int("".join([x for x in distance.split()[1:]]))
    
    y = 0
    for hold in range(time):
        dist = (time-hold)*hold
        if dist > distance:
            y += 1
    return y

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))