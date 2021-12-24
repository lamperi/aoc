import os.path
from heapq import heappop, heappush

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

test = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""

goalstate = """#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########"""

easytest = """#############
#..........A#
###.#B#C#D###
  #A#B#C#D#  
  #########"""

INSERT = """  #D#C#B#A#
  #D#B#A#C#"""

GOALS = {
    'A': ((5, 3), (4, 3), (3, 3), (2, 3)),
    'B': ((5, 5), (4, 5), (3, 5), (2, 5)),
    'C': ((5, 7), (4, 7), (3, 7), (2, 7)),
    'D': ((5, 9), (4, 9), (3, 9), (2, 9)),
}
COST = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}
WAITS = (
    (1, 1),
    (1, 2),
    (1, 4),
    (1, 6),
    (1, 8),
    (1, 10),
    (1, 11),
)
WAITS_SET = set(WAITS)

def gen_steps(start_pos, goal_pos):
    y, x = start_pos
    if start_pos[0] > goal_pos[0]:
        dir = 1 if goal_pos[0] > start_pos[0] else -1
        while y != goal_pos[0]:
            y += dir
            yield y,x
        dir = 1 if goal_pos[1] > start_pos[1] else -1
        while x != goal_pos[1]:
            x += dir
            yield y,x
    else:
        dir = 1 if goal_pos[1] > start_pos[1] else -1
        while x != goal_pos[1]:
            x += dir
            yield y,x
        dir = 1 if goal_pos[0] > start_pos[0] else -1
        while y != goal_pos[0]:
            y += dir
            yield y,x

def count_steps(start_pos, goal_pos, amphipod_pos):
    # two ways to move: to hallway
    if any(step in amphipod_pos for step in gen_steps(start_pos, goal_pos)):
        return False
    return abs(start_pos[0]-goal_pos[0]) + abs(start_pos[1]-goal_pos[1])

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
    s = ''
    max_y = max(y for y, _ in area.keys())
    max_x = max(x for _, x in area.keys())
    for y in range(0, max_y+1):
        for x in range(0, max_x+1):
            c = amphipod_pos.get((y, x), None)
            if c is None:
                c = area.get((y, x), ' ')
                if c in 'ABCD':
                    c = '.'
            s += c
        s += '\n'
    print(s)


def get_reachable_wait_pos(start_pos, pos_set):
    y,x = start_pos
    ok = True
    while y != 1:
        y -= 1
        if (y,x) in pos_set:
            ok = False
            break
    if not ok:
        return
    while x > 0:
        x -= 1
        if (y,x) in pos_set:
            break
        elif (y,x) in WAITS_SET:
            yield (y,x)
    x = start_pos[1]
    while x < 12:
        x += 1
        if (y,x) in pos_set:
            ok = False
            break
        elif (y,x) in WAITS_SET:
            yield (y,x)
    

def part2(data, insert=True, print_path=False):
    area = {}
    if insert:
        lines = data.splitlines()
        data = '\n'.join(lines[:3] + INSERT.splitlines() + lines[3:])
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            area[(y, x)] = c
    # state is (A1, A2, A3, A4, B1, B2, B3, B4, C1, C2, C3, C5, D1, D2, D3, D4)
    state = (
        0,  # cost
        tuple(sorted(c for c, t in area.items() if t == 'A')) +
        tuple(sorted(c for c, t in area.items() if t == 'B')) +
        tuple(sorted(c for c, t in area.items() if t == 'C')) +
        tuple(sorted(c for c, t in area.items() if t == 'D'))
    )
    count_per_type = len(state[1])//4
    goals = {k: v[-count_per_type:] for k, v in GOALS.items()}
    visited_states = {state: (None, None)}
    heap = [state]
    rounds = 0
    types = [chr(ord('A') + i//count_per_type) for i in range(4*count_per_type)]
    type_slices = [
        slice(count_per_type*(i//count_per_type), count_per_type*(i//count_per_type)+count_per_type)
        for i in range(4*count_per_type)]
    prev = {}
    while heap:
        rounds += 1
        optimal_moves = []
        non_optimal_moves = []
        energy, pos = heappop(heap)
        pos_set = set(pos)
        goal_tile = 0
        for i, p in enumerate(pos):
            t = types[i]
            tile_pos = pos[type_slices[i]]
            if p in goals[t]:
                already_filled_goals = [c for c in goals[t] if c[0] >= p[0]]
                if all(c in tile_pos for c in already_filled_goals):
                    if len(already_filled_goals) == len(goals[t]):
                        goal_tile += 1
                    continue
            # Case 1: our amphipod is in goal area
            if p[0] > 1:
                for (y,x) in get_reachable_wait_pos(p, pos_set):
                    steps = abs(p[0]-y) + abs(p[1]-x) 
                    energy_cost = steps * COST[t]
                    new_pos = pos_replace_sort(pos, i, (y,x))
                    new_state = (energy+energy_cost, new_pos)
                    if new_state not in visited_states:
                        visited_states[new_state] = (energy, pos)
                        non_optimal_moves.append(new_state)
            else:
                # Case 2: our amphipod is not in goal area
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
                steps = count_steps(p, goal_pos, pos_set)
                if steps != False:
                    energy_cost = steps * COST[t]
                    new_pos = pos_replace_sort(pos, i, goal_pos)
                    new_state = (energy+energy_cost, new_pos)
                    if new_state not in visited_states:
                        visited_states[new_state] = energy, pos
                        optimal_moves.append(new_state)
                        break
        if optimal_moves:
            for move in optimal_moves:
                heappush(heap, move)
            # no need to search the non-optimal moves if optimal moves exist
            continue
        for move in non_optimal_moves:
            heappush(heap, move)
        if goal_tile == 4:
            e = energy
            if print_path:
                path = []
                while pos != None:
                    path.append(pos)
                    e, pos = visited_states[(e,pos)]
                print("print path of length", len(path))
                for pos in reversed(path):
                    print_area(area, pos)
                    pass
                print("printed")
            return energy
    assert False, 'unsolvable'


def part1(state): return part2(state, insert=False)


assert(part1(goalstate) == 0)
assert(part1(easytest) == 9)
assert(part1(test) == 12521)
print(part1(data))

assert(part2(test) == 44169)
print(part2(data, print_path=True))
