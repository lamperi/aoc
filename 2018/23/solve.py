import re
from collections import deque
from heapq import heappop, heappush
import itertools

data = open('input.txt').read()

def manhattan(bot1, bot2):
    return abs(bot1[0]-bot2[0]) + abs(bot1[1] - bot2[1]) + abs(bot1[2] - bot2[2])

def get_count(pos, nanobots):
    c = 0
    for nanobot in nanobots:
        if manhattan(pos, nanobot) <= nanobot[3]:
            c += 1
    return c

def get_adj(pos):
    for distance in (10000000, 1000000, 100000, 10000, 1000, 100, 10, 1):
        # Faster subset of d that was worked best for my part 2
        #for d in ((0,-1,-1), (-1,0,0), (1,0,0), (0,-1,0), (0,1,0), (0,0,-1), (0,0,1)):

        # This should probably be better for all inputs (and example doesn't work without this)
        for d in itertools.product((-1,0,1), repeat=3):
            yield pos[0]+d[0]*distance, pos[1]+d[1]*distance, pos[2]+d[2]*distance

def parse(input_data):
    nanobots = []
    for line in input_data.splitlines():
        x,y,z,r = list(map(int, re.findall(r'-?\d+', line)))
        nanobots.append((x,y,z,r))
    return nanobots

def solve1(input_data):
    nanobots = parse(input_data)

    max_r = 0
    max_nanobot = None
    for nanobot in nanobots:
        if nanobot[3] > max_r:
            max_r = nanobot[3]
            max_nanobot = nanobot

    part1_c = 0
    for nanobot in nanobots:
        if manhattan(max_nanobot, nanobot) <= max_nanobot[3]:
            part1_c += 1
    return part1_c

def solve2(input_data, debug=False):
    nanobots = parse(input_data)
    queue = [(0, 0, 0, 0, 0)]
    visited = set([(0, 0, 0)])
    min_count_dist = (0, 0)
    since_best = 0
    while queue:
        count, dist, *pos = heappop(queue)
        if (count, dist) < min_count_dist:
            min_count_dist = (count, dist)
            if debug:
                print('Found',count,'at',pos,'manhattan',dist)
            since_best = 0
        else:
            since_best += 1
            # Constant 50 found by guessing - solved by using debug and waiting enough
            if since_best > 50:
                break
        for adj_pos in get_adj(pos):
            if adj_pos not in visited:
                visited.add(adj_pos)
                adj_count = get_count(adj_pos, nanobots)
                adj_dist = manhattan((0,0,0), adj_pos)
                heappush(queue, (-adj_count, adj_dist, *adj_pos))
    return min_count_dist[1]

print(solve1("""pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1"""))
print(solve2("""pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5"""))

print(solve1(data))
print(solve2(data))