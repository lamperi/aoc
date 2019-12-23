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
        if opcode == 3:
            # Have to do extra breaks for this "concurrent" exercise
            yield None
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
def solve(intcode):
    networking = []
    computer = []
    output = []
    def input_logic(input_list):
        while True:
            if input_list:
                yield input_list.pop(0)
            else:
                yield -1

    for i in range(50):
        output.append([])
        networking.append([i])
        computer.append(run_yield(intcode[:], input_logic(networking[i])))
    
    while True:
        for i in range(50):
            while True:
                nv = next(computer[i])
                if nv is None:
                    break
                output[i].append(nv)
                #print("output",i,"is",len(output[i]))
                if len(output[i]) == 3:
                    t = output[i].pop(0)
                    x = output[i].pop(0)
                    y = output[i].pop(0)
                    if t == 255:
                        return y
                    networking[t].extend([x,y])

def solve2(intcode):
    networking = []
    computer = []
    output = []
    last_read_empty = []
    def input_logic(input_list, empty_read):
        while True:
            if input_list:
                yield input_list.pop(0)
                empty_read[0] = False
            else:
                yield -1
                empty_read[0] = True

    for i in range(50):
        output.append([])
        networking.append([i])
        last_read_empty.append([False])
        computer.append(run_yield(intcode[:], input_logic(networking[i], last_read_empty[i])))
    
    nat = None
    nat_y = set()
    while True:
        for i in range(50):
            while True:
                nv = next(computer[i])
                if nv is None:
                    break
                output[i].append(nv)
                if len(output[i]) == 3:
                    t = output[i].pop(0)
                    x = output[i].pop(0)
                    y = output[i].pop(0)
                    if t == 255:
                        nat = (x, y)
                    else:
                        networking[t].extend([x,y])
        if all(e[0] for e in last_read_empty) and all(len(n) == 0 for n in networking):
            if nat is not None:
                x,y = nat
                if y in nat_y:
                    return y
                nat_y.add(y)
                networking[0].extend(nat)


print(solve(intcode))
print(solve2(intcode))