import os.path
from collections import Counter, defaultdict
from itertools import combinations
from operator import add, sub

INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

INPUT=os.path.join(os.path.dirname(__file__), "test_input.txt")
with open(INPUT) as f:
    test = f.read()

def orientations(xyz):
    # x up
    yield xyz[0], xyz[1], xyz[2]
    yield xyz[0], xyz[2], -xyz[1]
    yield xyz[0], -xyz[1], -xyz[2]
    yield xyz[0], -xyz[2], xyz[1]
    # x down
    yield -xyz[0], xyz[2], xyz[1]
    yield -xyz[0], xyz[1], -xyz[2]
    yield -xyz[0], -xyz[2], -xyz[1]
    yield -xyz[0], -xyz[1], xyz[2]
    # x right
    yield xyz[2], xyz[0], xyz[1]
    yield xyz[2], xyz[1], -xyz[0]
    yield xyz[2], -xyz[0], -xyz[1]
    yield xyz[2], -xyz[1], xyz[0]
    # x left
    yield -xyz[2], xyz[1], xyz[0]
    yield -xyz[2], xyz[0], -xyz[1]
    yield -xyz[2], -xyz[1], -xyz[0]
    yield -xyz[2], -xyz[0], xyz[1]
    # x forward
    yield xyz[1], xyz[2], xyz[0]
    yield xyz[1], xyz[0], -xyz[2]
    yield xyz[1], -xyz[2], -xyz[0]
    yield xyz[1], -xyz[0], xyz[2]
    # x backward
    yield -xyz[1], xyz[0], xyz[2]
    yield -xyz[1], xyz[2], -xyz[0]
    yield -xyz[1], -xyz[0], -xyz[2]
    yield -xyz[1], -xyz[2], xyz[0]

assert(len(set(orientations(range(3))))) == 24

def part12(data):
    scanners=defaultdict(list)
    for id, scanner in enumerate(data.split("\n\n")):
        _, *rest = scanner.splitlines()
        for line in rest:
            x,y,z = line.split(",")
            scanners[id].append((int(x),int(y),int(z)))
    coords = {0: (0,0,0)}
    beacons = set(scanners[0])
    to_match = set(scanners.keys()) - set(coords.keys())
    
    while to_match:
        for scanner_id in to_match:
            matched_coords=Counter()
            for beacon in beacons:
                for xyz in scanners[scanner_id]:
                    for oi, o in enumerate(orientations(xyz)):
                        t = tuple(map(sub, beacon, o)), oi
                        matched_coords[t] += 1
            (coord, matched_orientation_index), count = matched_coords.most_common(1)[0]
            if count < 12:
                continue
            to_match.remove(scanner_id)
            coords[scanner_id] = coord
            for xyz in scanners[scanner_id]:
                for oi, o in enumerate(orientations(xyz)):
                    if oi != matched_orientation_index:
                        continue
                    beacons.add(tuple(map(add, coord, o)))
            break  # to mark a match and to fix iterator invalidation
        else:
            # Not able to solve
            assert False

    # PART 2
    max_distance = max(
        sum(map(lambda a,b: abs(b-a), s1, s2))
        for s1, s2 in combinations(coords.values(), 2))
    
    return len(beacons), max_distance

print((79, 3621), part12(test))
print(part12(data))

