import os.path
from itertools import pairwise
import re

FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(FILE) as f:
    INPUT = f.read()

def ints(line):
    return map(int, re.findall("-?\d+", line))

TEST = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

def parse(data):
    sensors = []
    beacons = set()
    for line in data.splitlines():
        sx,sy,bx,by = list(ints(line))
        dist = abs(sx-bx) + abs(sy-by)
        sensors.append((sx,sy,bx,by,dist))
        beacons.add((bx,by))
    return sensors, beacons


def find_blocked_ranges(sensors, coord, value_interest):
    ranges = []
    other_coord = 1-coord
    for sx,sy,_,_,dist in sensors:
        s = (sx,sy)
        dc = abs(s[coord] - value_interest)
        reach = dist - dc
        if reach < 0:
            continue
        blocked_values = (s[other_coord] - reach, s[other_coord] + reach)

        overlapping = []
        smaller_index = len(ranges)
        for i,r in enumerate(ranges):
            if not (r[0] > blocked_values[1] or r[1] < blocked_values[0]):
                overlapping.append(i)
            if blocked_values[0] < r[0]:
                smaller_index = min(smaller_index, i)
        if overlapping:
            merged = (min(blocked_values[0], ranges[overlapping[0]][0]), max(blocked_values[1], ranges[overlapping[-1]][1]))
            del ranges[overlapping[0]:overlapping[-1]+1]
            ranges.insert(overlapping[0], merged)
        else:
            ranges.insert(smaller_index, blocked_values)
        #print("new ranges",ranges)

    beacons_at_line = set((x,y)[other_coord] for _,_,x,y,_ in sensors if (x,y)[coord] == value_interest)
    for c in beacons_at_line:
        new_ranges = []
        for r in ranges:
            if r[0] <= c <= r[1]:
                if r[0] < c:
                    new_ranges.append((r[0], c-1))
                if c < r[1]:
                    new_ranges.append((c+1, r[1]))
            else:
                new_ranges.append(r)
        ranges = new_ranges
    return ranges

# PART 1
def solve(data, y_coordinate):
    sensors, _ = parse(data)
    ranges = find_blocked_ranges(sensors, 1, y_coordinate)
    l = 0
    for r in ranges:
        l += r[1] - r[0] + 1
    return l

print(solve(TEST, 10))
print(solve(INPUT, 2000000))

# PART 2
def find_gaps(ranges, min, max):
    cur = min
    for r in ranges:
        for x in range(cur, r[0]):
            if x <= max:
                yield x
            else:
                return
        cur = r[1]+1

def solve2(data, min_xy, max_xy):
    sensors = []
    beacons = set()
    for line in data.splitlines():
        sx,sy,bx,by = list(ints(line))
        dist = abs(sx-bx) + abs(sy-by)
        sensors.append((sx,sy,bx,by,dist))
        beacons.add((bx,by))
    y_ranges = []  # impossible x locations by index y
    for y in range(min_xy, max_xy+1):
        py = find_blocked_ranges(sensors, 1, y)
        y_ranges.append(py)
    x_ranges = []  # impossible y locations by index x
    for x in range(min_xy, max_xy+1):
        px = find_blocked_ranges(sensors, 0, x)
        x_ranges.append(px)
    for y in range(min_xy, max_xy+1):
        for x in find_gaps(y_ranges[y], min_xy, max_xy):
            valid_y = True
            for yr in x_ranges[x]:
                if yr[0] <= y <= yr[1]:
                    valid_y = False
            if valid_y and (x,y) not in beacons:
                return x * 4000000 + y

print(solve2(TEST, 0, 20))
print(solve2(INPUT, 0, 4000000))
