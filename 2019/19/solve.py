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
            'op': lambda: next(get_input),
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

def solve1(intcode):
    o = []
    for y in range(50):
        for x in range(50):
            o.append(run_coord(intcode, y, x))
    return sum(o)

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
            if val == 0:
                val = "."
            elif val == 1:
                val = "#"
            elif val == 2:
                val = "O"
            row.append(val)
        image.append("".join(row))

    print("Y:[{}, {}] X:[{},{}]".format(min_y, max_y, min_x, max_x))
    print("\n".join(image))

def run_coord(intcode, y, x):
    def gen():
        yield x
        yield y
    for output in run_yield(intcode[:], gen()):
        return output

def solve2(intcode):
    area = {}
    for y in range(30):
        for x in range(30):
            block = run_coord(intcode, y, x)
            area[(y,x)] = block
    #print_area(area)
    max_y = max(y for (y,x),v in area.items())
    xx = [x for (y,x),v in area.items() if y == max_y and v == 1]
    min_x = min(xx)
    max_x = max(xx)
    tries = 0
    smoke_passed = 0
    while max_y < 100000:
        max_y += 1
        min_x -= 1
        block = 0
        while block == 0:
            block = run_coord(intcode, max_y, min_x)
            area[(max_y,min_x)] = block
            min_x += 1
        min_x -= 1
        block = 1
        while block == 1:
            block = run_coord(intcode, max_y, max_x)
            area[(max_y,max_x)] = block
            max_x += 1
        max_x -= 2
        W=100
        gap = max_x-min_x
        if gap >= W:
            min_y = max_y - W + 1
            tries += 1
            b0 = run_coord(intcode, max_y, min_x-1)
            assert b0 == 0
            # smoketest
            if smoke_test(intcode, max_y, min_x, W):
                smoke_passed += 1
                bb = [run_coord(intcode, y, x) for y,x in gen_frame(min_y, min_x, W)]
                if all(b == 1 for b in bb):
                    for y,x in gen_frame(min_y, min_x, W):
                        area[(y,x)] = 2
                    #print_area({a:b for a,b in area.items() if a[0] >= max_y-W-3})
                    return min_y + 10000 * min_x
    
def gen_frame(min_y, min_x, W):
    for y in range(min_y, min_y+W):
        yield (y, min_x)
        yield (y, min_x+W-1)
    for x in range(min_x, min_x+W):
        yield (min_y, x)
        yield (min_y+W-1, x)

def smoke_test(intcode, y, x, W):
    b1 = run_coord(intcode, y, x)
    b2 = run_coord(intcode, y-W+1, x)
    b3 = run_coord(intcode, y-W+1, x+W-1)
    b4 = run_coord(intcode, y, x+W-1)
    return all(b == 1 for b in (b1,b2,b3,b4))

print(solve1(intcode))
print(solve2(intcode))