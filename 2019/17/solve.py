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

def adj(area, y, x):
    if y > 0:
        yield area[y-1][x]
    if x > 0:
        yield area[y][x-1]
    if y+1 < len(area):
        yield area[y+1][x]
    if x+1 < len(area[y]):
        yield area[y][x+1]


def solve(intcode):
    o = []
    for output in run_yield(intcode[:], lambda: 0):
        o.append(chr(output))
    area_str = "".join(o)
    area = area_str.splitlines()[:-1]
    intersections = []
    for y, line in enumerate(area):
        for x, c in enumerate(line):
            if c == "#" and sum(1 for a in adj(area, y,x) if a == "#") == 4:
                intersections.append((y,x))
    print(sum((y*x) for y,x in intersections))

    # Part 2
    intcode[0] = 2
    # Carefully optimized hand-written code 
    main = "A,B,B,A,C,A,C,A,C,B"
    A = "L,6,R,12,R,8"
    B = "R,8,R,12,L,12"
    C = "R,12,L,12,L,4,L,4"
    debug = "n"
    assert len(main) <= 20
    assert len(A) <= 20
    assert len(B) <= 20
    assert len(C) <= 20
    inst = "\n".join([main, A, B, C, debug, ""])
    ptr = [0]

    def movement_logic():
         o = ord(inst[ptr[0]])
         ptr[0] += 1
         return o
    o = []
    for output in run_yield(intcode[:], movement_logic):
        o.append(output)
        if len(o) > 2 and o[-2] == 10 and o[-1] == 10:
            print("".join(chr(c) for c in o[:-1]))
            o = []
    print("".join(chr(c) for c in o[:-1]))
    return o[-1]
    

print(solve(intcode))