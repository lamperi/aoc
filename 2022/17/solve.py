import os.path
from itertools import pairwise
import re

FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(FILE) as f:
    INPUT = f.read()

def ints(line):
    return map(int, re.findall("-?\d+", line))

TEST = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""

def create_rock(bottom, shape):
    if shape == 0:
        return [(3,bottom),(4,bottom),(5,bottom),(6,bottom)]
    elif shape == 1:
        return [(4,bottom),(3,bottom+1),(4,bottom+1),(5,bottom+1),(4,bottom+2)]
    elif shape == 2:
        return [(3,bottom),(4,bottom),(5,bottom),(5,bottom+1),(5,bottom+2)]
    elif shape == 3:
        return [(3,bottom),(3,bottom+1),(3,bottom+2),(3,bottom+3)]
    else:
        return [(3,bottom),(4,bottom),(3,bottom+1),(4,bottom+1)]

def print_walls(walls):
    y = max(y for _,y in walls)
    s = [""]
    while y >= 1:
        l = "|"
        for x in range(1,8):
            l += "#" if (x,y) in walls else "."
        l += "|"
        s.append(l)
        y -= 1
    s.append("+-------+")
    print("\n".join(s))

def solve(data):
    pat = data.strip()

    top = 0
    walls = set((x,0) for x in range(0, 8))
    time = 0
    for rock_index in range(2022):
        shape = rock_index % 5
        rock_cells = create_rock(top+4, shape)
        #if rock_index < 6:
        #    print_walls(walls)
        while True:
            if pat[time % len(pat)] == "<":
                if min(x for x,_ in rock_cells) == 1:
                    new_rock_cells = rock_cells[:]
                else:
                    new_rock_cells = [(x-1,y) for x,y in rock_cells]
                    if any(c in walls for c in new_rock_cells):
                        new_rock_cells = rock_cells[:]
            else:
                if max(x for x,_ in rock_cells) == 7:
                    new_rock_cells = rock_cells[:]
                else:
                    new_rock_cells = [(x+1,y) for x,y in rock_cells]
                    if any(c in walls for c in new_rock_cells):
                        new_rock_cells = rock_cells[:]
            down_rock_cells = [(x,y-1) for x,y in new_rock_cells]
            time += 1
            if any(c in walls for c in down_rock_cells):
                for c in new_rock_cells:
                    walls.add(c)
                top = max(top, max(y for _,y in new_rock_cells))
                break
            rock_cells = down_rock_cells

    return top 

print(solve(TEST))
print(solve(INPUT))


def solve2(data):
    pat = data.strip()

    top = 0
    walls = set((x,0) for x in range(0, 8))
    time = 0
    most_under_top = 0

    state = {}
    state_lines = 28
    max_rocks = 1000000000000
    rock_index = 0
    skipped = False
    while rock_index < max_rocks:
        shape = rock_index % 5

        walls = set((x,y) for x,y in walls if y >= top-state_lines)
        if not skipped and top > state_lines:
            state_walls = frozenset((x,y-top) for x,y in walls)
            st = (time % len(pat), state_walls, shape)
            if st in state:
                loop_length_t = time - state[st][0]
                loop_length_top = top - state[st][1]
                loop_length_r = rock_index - state[st][2]
                #print(f"LOOP from {(time, top, rock_index)} to {state[st]}")
                #print(f"LOOP LENGTH {loop_length_t}, {loop_length_r}")
                iterations_skipped = (max_rocks - rock_index)//loop_length_r
                #print(f"LOOP skipping {iterations_skipped}")
                rock_index += loop_length_r * iterations_skipped
                time += loop_length_t * iterations_skipped
                top_skip = loop_length_top * iterations_skipped
                walls = set((x,y+top_skip) for x,y in walls)
                top += top_skip
                #print(f"LOOP after: {(time, top, rock_index)}")
                skipped = True
            state[st] = (time, top, rock_index)

        rock_cells = create_rock(top+4, shape)
        while True:
            if pat[time % len(pat)] == "<":
                if min(x for x,_ in rock_cells) == 1:
                    new_rock_cells = rock_cells[:]
                else:
                    new_rock_cells = [(x-1,y) for x,y in rock_cells]
                    if any(c in walls for c in new_rock_cells):
                        new_rock_cells = rock_cells[:]
            else:
                if max(x for x,_ in rock_cells) == 7:
                    new_rock_cells = rock_cells[:]
                else:
                    new_rock_cells = [(x+1,y) for x,y in rock_cells]
                    if any(c in walls for c in new_rock_cells):
                        new_rock_cells = rock_cells[:]
            down_rock_cells = [(x,y-1) for x,y in new_rock_cells]
            time += 1
            if any(c in walls for c in down_rock_cells):
                for c in new_rock_cells:
                    walls.add(c)

                top_from_rock = max(y for _,y in new_rock_cells)
                """
                # THIS Part was used to estimate variable state_lines
                # Essentially, we wanted a reproducible and a smallish state of top rocks.
                # 
                
                if top - top_from_rock > most_under_top:
                    most_under_top = top - top_from_rock
                    #print("record under top:", most_under_top)
                    if most_under_top == 23:
                        most_under_top = 0
                
                """
                top = max(top, top_from_rock)
                break
            rock_cells = down_rock_cells
        rock_index += 1
    return top 

# For test case most_under_top = 5
# For input 23

print(solve2(TEST))
print(solve2(INPUT))
