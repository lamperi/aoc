with open("input.txt") as f:
    data = f.read().strip()
intcode = [int(a) for a in data.split(",")]

from collections import defaultdict
from random import choice

def run_yield(nums, get_input):
    ops = {
        1: {
            'in': 2,
            'out': 1,
            'op': lambda a, b: a+b,
        },
        2: {
            'in': 2,
            'out': 1,
            'op': lambda a, b: a*b,
        },
        3: {
            'in': 0,
            'out': 1,
            'op': lambda: get_input(),
        },
        4: {
            'in': 1,
            'out': 0,
            'op': lambda a: OUTPUT.append(a),
            'yield': True,
        },
        5: {
            'in': 2,
            'out': 0,
            'op': lambda a, b: b if a != 0 else None,
            'jump': True,
        },
        6: {
            'in': 2,
            'out': 0,
            'op': lambda a, b: b if a == 0 else None,
            'jump': True,
        },
        7: {
            'in': 2,
            'out': 1,
            'op': lambda a,b: 1 if a < b else 0,
        },
        8: {
            'in': 2,
            'out': 1,
            'op': lambda a,b: 1 if a == b else 0,
        },
        9: {
            'in': 1,
            'out': 0,
            'op': lambda a: a,
            'rel': True,
        },
        99: {
            'in': 0,
            'out': 0,
            'op': lambda: None,
            'exit': True,
        },
    }

    pc = 0
    rel = 0
    OUTPUT = []
    # Unlimited memory
    nums = defaultdict(lambda: 0, enumerate(nums))
    while True:
        opcode = nums[pc] % 100
        val = int(nums[pc] / 100)
        i, j, k = int(val/100), int(val/10)%10, val%10
        if opcode in ops:
            mode = [k, j, i]
            mode_index = 0
            inputs = []
            for input_n in range(1, ops[opcode]['in']+1):
                a = nums[pc+input_n]
                if mode[mode_index] == 0:
                    a = nums[a]
                elif mode[mode_index] == 1:
                    pass
                elif mode[mode_index] == 2:
                    a = nums[a + rel]
                mode_index += 1
                inputs.append(a)
            out = ops[opcode]['op'](*inputs)
            if ops[opcode]['out'] == 1:
                a = nums[pc+1+ops[opcode]['in']]
                if mode[mode_index] == 0:
                    nums[a] = out
                elif mode[mode_index] == 1:
                    pass
                elif mode[mode_index] == 2:
                    nums[a + rel] = out
                mode_index += 1
            if ops[opcode].get('yield', False):
                yield OUTPUT[-1]
            if ops[opcode].get('rel', False):
                rel += out
            if ops[opcode].get('exit', False):
                break
            if ops[opcode].get('jump', False) and out is not None:
                pc = out
            else:
                pc += 1 + ops[opcode]['in'] + ops[opcode]['out'] 
        else:
            raise Exception('opcode={}'.format(opcode))
    return OUTPUT

# END OF INTCODE INTERPRETER

def print_area(area):
    image = []
    min_x = min(x for y,x in area.keys())
    max_x = max(x for y,x in area.keys())
    min_y = min(y for y,x in area.keys())
    max_y = max(y for y,x in area.keys())
    for y in range(min_y, max_y+1):
        row = []
        for x in range(min_x, max_x+1):
            val = area.get((y,x), " ")
            row.append(val)
        image.append("".join(row))

    print("Y:[{}, {}] X:[{},{}]".format(min_y, max_y, min_x, max_x))
    print("\n".join(image))


def dir_to_pos(dir):
    return {1: (-1, 0), 2: (1, 0), 3: (0, 1), 4: (0, -1)}[dir]

def pos_sum(x,y):
    return x[0] + y[0], x[1] + y[1]

def bfs(area, goal, pos):
    visited = {pos: 0}
    l = [pos]
    while l:
        p = l[0]
        l = l[1:]
        for y,x in (pos_sum(p, dir_to_pos(i)) for i in (1,2,3,4)):
            if (y,x) in visited:
                continue
            if area.get((y,x), "#") != "#":
                l.append((y,x))
                visited[(y,x)] = visited[p] + 1
                if (y,x) == goal:
                    return visited[(y,x)]

def bfs_full(area, pos):
    visited = {pos: 0}
    l = [pos]
    while l:
        p = l[0]
        l = l[1:]
        for y,x in (pos_sum(p, dir_to_pos(i)) for i in (1,2,3,4)):
            if (y,x) in visited:
                continue
            if area.get((y,x), "#") != "#":
                l.append((y,x))
                visited[(y,x)] = visited[p] + 1
    return max(visited.values())

def return_dir(dir):
    return {1: 2, 2: 1, 3: 4, 4: 3,None:None}[dir]

def solve(intcode):
    area = {}
    area[(0,0)] = "D"
    pos = 0, 0  # y, x
    opos = None
    last_input = [None]
    dfs_state = {}

    def input_func():
        if pos not in dfs_state:
            unvisited = []
            for i in (1,2,3,4):
                y,x = pos_sum(pos, dir_to_pos(i))
                if area.get((y,x), " ") == " ":
                    unvisited.append(i)
            dfs_state[pos] = {
                'backtrack': return_dir(last_input[0]),
                'unvisited': unvisited,
                'unvisited_index': 0,
            }
        state = dfs_state[pos]
        if state['unvisited_index'] == len(state['unvisited']):
            last_input[0] = state['backtrack']
        else:
            last_input[0] = state['unvisited'][state['unvisited_index']]
            state['unvisited_index'] += 1
        # Special case: we have mapped the whole area, just return something valid
        if last_input[0] is None:
            return 1
        return last_input[0]
    
    for t, reply in enumerate(run_yield(intcode, input_func)):
        # Quit when all of the area has been mapped
        if last_input[0] is None:
            break
        if reply == 0:
            c = pos_sum(pos, dir_to_pos(last_input[0]))
            area[c] = "#"
        elif reply == 1:
            area[pos] = "."
            pos = pos_sum(pos, dir_to_pos(last_input[0]))
            area[pos] = "D"
        elif reply == 2:
            area[pos] = "."
            pos = pos_sum(pos, dir_to_pos(last_input[0]))
            area[pos] = "D"
            opos = pos
        else:
            raise Exception("Unknown reply {}".format(reply))

    print("Final map after BFS of {} iterations".format(t))
    area[(0,0)] = "S"
    area[opos] = "O"
    print_area(area)
    print()

    goal = opos
    pos = 0, 0
    print("Solve BFS from {} to {}".format(pos, goal))

    p1 = bfs(area, goal, pos)
    p2 = bfs_full(area, goal)

    return p1, p2


print(solve(intcode))