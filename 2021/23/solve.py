import operator
from os import X_OK
import os.path
import re
from collections import Counter, defaultdict, deque
from functools import partial, reduce
from heapq import heappop, heappush
from io import TextIOBase
from itertools import combinations, count, pairwise, permutations
from math import isfinite, prod

INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

test="""#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""

goalstate="""#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########"""

easytest="""#############
#..........A#
###.#B#C#D###
  #A#B#C#D#  
  #########"""

INSERT = """  #D#C#B#A#
  #D#B#A#C#"""

GOALS = {
    'A': ((5,3),(4,3),(3,3),(2,3)),
    'B': ((5,5),(4,5),(3,5),(2,5)),
    'C': ((5,7),(4,7),(3,7),(2,7)),
    'D': ((5,9),(4,9),(3,9),(2,9)),
}
COST = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}
WAITS = (
    (1,1),
    (1,2),
    (1,4),
    (1,6),
    (1,8),
    (1,10),
    (1,11),
)

def count_steps(start_pos, goal_pos, amphipod_pos):
    amphipod_pos = set(amphipod_pos)
    # two ways to move: to hallway
    steps = 0
    assert start_pos[0] != goal_pos[0]
    if start_pos[0] > goal_pos[0]:
        y,x = start_pos
        while y > goal_pos[0]:
            y -= 1
            steps += 1
            if (y,x) in amphipod_pos:
                return False
        dir = 1 if goal_pos[1] > start_pos[1] else -1
        while x != goal_pos[1]:
            x += dir
            steps += 1
            if (y,x) in amphipod_pos:
                return False
        assert (y,x) == goal_pos
        return steps
    else:
        y,x = start_pos
        dir = 1 if goal_pos[1] > start_pos[1] else -1
        while x != goal_pos[1]:
            x += dir
            steps += 1
            if (y,x) in amphipod_pos:
                return False
        while y != goal_pos[0]:
            y += 1
            steps += 1
            if (y,x) in amphipod_pos:
                return False
        assert (y,x) == goal_pos
        return steps

def pos_replace_sort(tup, index, value):
    new_tuple = tup[:index] + (value,) + tup[index+1:]
    nr_per_type = len(tup)//4
    new_tuple = (new_tuple[:nr_per_type*(index//nr_per_type)] +
        tuple(sorted(new_tuple[nr_per_type*(index//nr_per_type):nr_per_type*(index//nr_per_type)+nr_per_type])) +
        new_tuple[nr_per_type*(index//nr_per_type)+nr_per_type:])
    assert len(new_tuple) == len(tup)
    return new_tuple

def print_area(area, pos):
    amphipod_pos = {}
    count_per_type = len(pos)//4
    for i, p in enumerate(pos):
        t = chr(ord('A') + i//count_per_type)
        amphipod_pos[p] = t
    s = ""
    max_y = max(y for y,_ in area.keys())
    max_x = max(x for _,x in area.keys())
    for y in range(0, max_y+1):
        for x in range(0, max_x+1):
            c = amphipod_pos.get((y,x), None)
            if c is None:
                c = area.get((y,x), " ")  
                if c in 'ABCD':
                    c = "."
            s += c
        s += "\n"
    print(s)

def part2(data, insert=True):
    area = {}
    if insert:
        lines = data.splitlines()
        data = "\n".join(lines[:3] + INSERT.splitlines() + lines[3:])
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            area[(y,x)] = c
    # state is (A1, A2, A3, A4, B1, B2, B3, B4, C1, C2, C3, C5, D1, D2, D3, D4)
    state = (
        0, # cost
        tuple(sorted(c for c,t in area.items() if t == 'A')) +
        tuple(sorted(c for c,t in area.items() if t == 'B')) + 
        tuple(sorted(c for c,t in area.items() if t == 'C')) +
        tuple(sorted(c for c,t in area.items() if t == 'D'))
    )
    count_per_type = len(state[1])//4
    goals = {k:v[-count_per_type:] for k,v in GOALS.items()}
    visited_states = {state}
    heap = [state]
    while heap:
        energy, pos = heappop(heap)
        #print_area(area, pos)
        goal_tile = 0
        for i, p in enumerate(pos):
            t = chr(ord('A') + i//count_per_type)
            tile_pos = pos[count_per_type*(i//count_per_type):count_per_type*(i//count_per_type)+count_per_type]
            if i % count_per_type == 0:
                if all(c in goals[t] for c in tile_pos):
                    goal_tile += 1
                    continue
            if p in goals[t]:
                already_filled_goals = [c for c in goals[t] if c[0] >= p[0]]
                if all(c in tile_pos for c in already_filled_goals):
                    continue
            if p[0] > 1:
                for coord in WAITS:
                    steps = count_steps(p, coord, pos)
                    if steps == False:
                        continue
                    energy_cost = steps * COST[t]
                    new_pos = pos_replace_sort(pos, i, coord)
                    new_state = (energy+energy_cost, new_pos)
                    if new_state not in visited_states:
                        visited_states.add(new_state)
                        heappush(heap, new_state)
            else:
                # First first goal pos:
                ok = True
                for goal_pos in goals[t]:
                    if goal_pos in tile_pos:
                        continue
                    if goal_pos in pos:
                        ok = False
                    break
                if not ok:
                    continue
                steps = count_steps(p, goal_pos, pos)
                if steps != False:
                    energy_cost = steps * COST[t]
                    new_pos = pos_replace_sort(pos, i, goal_pos)
                    new_state = (energy+energy_cost, new_pos)
                    if new_state not in visited_states:
                        visited_states.add(new_state)
                        heappush(heap, new_state)

        if goal_tile == 4:
            return energy
    assert False, "unsolvable"


part1 = lambda state: part2(state, insert=False)
assert(part1(goalstate) == 0)
assert(part1(easytest) == 9)
assert(part1(test) == 12521)
print(part1(data))

assert(part2(test) == 44169)
print(part2(data))

