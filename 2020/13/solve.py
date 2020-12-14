import os.path
import collections
import re
import math
import itertools
INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

def solve(data):
    lines = data.split("\n")
    earliest_time = int(lines[0])
    bus_lines = lines[1].split(",")
    min_wait_time = None
    best_bus = None
    for bus_line in bus_lines:
        if bus_line == "x":
            continue
        bus = int(bus_line)
        # bus goes every "bus" minutes, starting from 0
        next_bus_arrival = bus*int(math.ceil(earliest_time/bus))
        wait_time = next_bus_arrival - earliest_time
        if min_wait_time is None or wait_time < min_wait_time:
            best_bus = bus
            min_wait_time = wait_time
    return best_bus, min_wait_time, best_bus*min_wait_time

print(solve("""939
7,13,x,x,59,x,31,19"""), 295)
print(solve(data))

def solve2(data):
    print()
    lines = data.split("\n")
    bus_lines = lines[1].split(",")
    constraints = []
    for t, bus_line in enumerate(bus_lines):
        if bus_line == "x":
            continue
        bus = int(bus_line)
        constraints.append((t, bus))
    multiplier = 1
    t0 = 0
    for t, bus in constraints:
        print(multiplier, t0, bus, t)
        gen = solutions(multiplier, bus, t0, t)
        t0 = next(gen)
        multiplier = next(gen)-t0
    stamp = t0
    for t, bus in constraints:
        assert (stamp + t) % bus == 0

    return stamp

def solutions(a, b, t0, t1):
    x = 1
    y = 1
    ret = 0
    while True:
        if a*x + t0 - b*y + t1 == 0:
            yield a*x + t0
            x += 1
            ret += 1
            if ret == 2:
                break
        elif a*x + t0  - b*y + t1 < 0:
            x += 1
        else:
            y += 1
            # Speedup: we will be here tomorrow if we increment by 1
            factor = 1
            while a*x + t0  - b*(factor+y) + t1 > 0:
                factor *= 17
            while factor >= 1:
                while a*x + t0  - b*(factor+y) + t1 > 0:
                    y += factor
                factor /= 17

print(solve2("""xxx
17,x,13,19"""), 3417)

print(solve2("""xxx
67,7,59,61"""), 754018)

print(solve2("""xxx
67,x,7,59,61"""), 779210)

print(solve2("""xxx
67,7,x,59,61"""), 1261476)

print(solve2("""xxx
1789,37,47,1889"""), 1202161486)

print(solve2("""xxx
7,13,x,x,59,x,31,19"""), 1068781)
print(solve2(data))
