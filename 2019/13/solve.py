with open("input.txt") as f:
    data = f.read().strip()
n = [int(a) for a in data.split(",")]

from collections import defaultdict

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

def pump3(iter):
    l = [None, None, None]
    for i, v in enumerate(iter):
        l[i%3] = v
        if i%3 == 2:
            yield tuple(l)

# PART 1
blocks_left = 0
m = defaultdict(dict)
for x,y,t in pump3(run_yield(n[:], lambda x: 0)):
    m[y][x] = t
    if t == 2:
       blocks_left += 1
print(blocks_left)

# PART 2
n[0] = 2
ball_x = 0
platform_x = 0
def give_input():
    if blocks_left == 0:
        return 0
    if platform_x < ball_x:
        return 1
    elif platform_x > ball_x:
        return -1
    return 0
m = defaultdict(dict)
score = 0
for x,y,t in pump3(run_yield(n[:], give_input)):
    m[y][x] = t
    if t == 3:
        platform_x = x
    if t == 4:
        ball_x = x
    if x == -1 and y == 0:
        score = t
        blocks_left = sum(1 for row in m.values() for x in row.values() if x == 2)      
print(score)
