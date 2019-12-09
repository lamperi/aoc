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
            'op': lambda a: OUTPUT.append(a)
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

print(run([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99], []))
print(run([1102,34915192,34915192,7,4,7,99,0], []))
print(run([104,1125899906842624,99], []))

print(run(n[:], [1]))
print(run(n[:], [2]))
