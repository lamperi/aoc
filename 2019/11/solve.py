with open("input.txt") as f:
    data = f.read().strip()
n = [int(a) for a in data.split(",")]

from collections import defaultdict

def run(nums, INPUT):
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
            'op': lambda: INPUT.pop(0)
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

def robot(n, o):
    INPUT = [o]
    sw = run(n, INPUT)
    d = -1, 0
    c = 0, 0
    colors = defaultdict(dict)
    painted = set()
    try:
        while True:
            color = next(sw)
            direction = next(sw)
            if color != 0 and color != 1:
                raise Exception("color")
            if direction != 0 and direction != 1:
                raise Exception("direction")
            colors[c[0]][c[1]] = 1 if color == 1 else 0
            painted.add(c)
            if direction == 0:
                d = -d[1], d[0]
            elif direction == 1:
                d = d[1], -d[0]
            c = c[0] + d[0], c[1] + d[1]
            INPUT.append(colors[c[0]].get(c[1], 0))
    except StopIteration:
        pass

    image = []
    min_x = 0
    max_x = 0
    for line in colors.values():
        xx = sorted(line.keys())
        if xx[0] < min_x:
            min_x = xx[0]
        if xx[-1] > max_x:
            max_x = xx[-1]
    for y in sorted(colors.keys()):
        line = colors[y]
        row = []
        for x in range(min_x, max_x+1):
            val = line.get(x, 0)
            row.append("#" if val == 1 else " ")
        image.append("".join(row))
    if o == 0:
        return len(painted)
    else:
        return "\n".join(image)
    


print(robot(n[:], 0))
print(robot(n[:], 1))

