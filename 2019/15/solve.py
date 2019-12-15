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

def print_area(area):
    image = []
    min_x = 0
    max_x = 0
    for line in area.values():
        xx = sorted(line.keys())
        if xx[0] < min_x:
            min_x = xx[0]
        if xx[-1] > max_x:
            max_x = xx[-1]
    for y in sorted(area.keys()):
        line = area[y]
        row = []
        for x in range(min_x, max_x+1):
            val = line.get(x, " ")
            row.append(val)
        image.append("".join(row))
    print("Y:[{}, {}] X:[{},{}]".format(min(area.keys()), max(area.keys()), min_x, max_x))
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
            if area[y].get(x, "#") != "#":
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
            if area[y].get(x, "#") != "#":
                l.append((y,x))
                visited[(y,x)] = visited[p] + 1
    return max(visited.values())

def solve(intcode):
    area = defaultdict(dict)
    area[0][0] = "D"
    pos = 0, 0  # y, x
    last_input = [None]

    def input_func():
        unvisited = []
        visited = []
        for i in (1,2,3,4):
            y,x = pos_sum(pos, dir_to_pos(i))
            if area[y].get(x, " ") == " ":
                unvisited.append(i)
            elif area[y].get(x, " ") != "#":
                visited.append(i)
        if unvisited:
            last_input[0] = choice(unvisited)
        else:
            last_input[0] = choice(visited)
        return last_input[0]
    
    for t, reply in enumerate(run_yield(intcode, input_func)):
        if reply == 0:
            y,x = pos_sum(pos, dir_to_pos(last_input[0]))
            area[y][x] = "#"
        elif reply == 1:
            area[pos[0]][pos[1]] = "."
            pos = pos_sum(pos, dir_to_pos(last_input[0]))
            area[pos[0]][pos[1]] = "D"
        elif reply == 2:
            area[pos[0]][pos[1]] = "."
            pos = pos_sum(pos, dir_to_pos(last_input[0]))
            area[pos[0]][pos[1]] = "O"
            break
        else:
            raise Exception("Unknown reply {}".format(reply))
        if t % 100000 == 0:
            print("Iterated {} rounds".format(t))

    print("Final map")
    area[0][0] = "S"
    print_area(area)
    print()

    goal = pos
    pos = 0, 0
    print("Solve DFS from {} to {}".format(pos, goal))

    p1 = bfs(area, goal, pos)
    p2 = bfs_full(area, goal)

    return p1, p2


print(solve(intcode))