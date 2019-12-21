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

def springscript(intcode, springscript):
    lines = []
    for line in springscript.splitlines():
        if line.find("#") != -1:
            line = line[:line.index("#")]
        line = line.strip()
        if line:
            lines.append(line)
    assert len(lines) <= 16
    lines.append("")
    inst = "\n".join(lines)
    print(inst)

    def movement_logic():
        for c in inst:
            yield ord(c)
    o = []
    for output in run_yield(intcode[:], movement_logic()):
        o.append(output)
        if len(o) > 2 and o[-2] == 10 and o[-1] == 10:
            print("".join(chr(c) for c in o[:-1]))
            o = []
    print("".join(chr(c) for c in o[:-1]))
    return o[-1] if len(o) else None

def solve(intcode):
    # Droid should jump:
    # D must be always ground
    # any of A, B, or C is a hole
    main = """
        NOT A J
        NOT B T
        OR T J
        NOT C T
        OR T J
        NOT D T  # D must always be ground
        NOT T T  # 2nd of line D
        AND T J
        WALK
    """
    part1 = springscript(intcode, main)
    print(part1)

    # Droid should jump:
    # D must be always ground
    # any of A, B, or C is a hole
    # In addition:
    # if E is a hole,
    # then also H must be ground

    # direct second jump <=> not E and H
    # impossible second jump <=> not E and not H
    # second jump uninteresting <=> E
    # cond = (second jump uninteresting) or (direct second jump) 
    #      = (E) or ((not E) and H)
    # not cond = (not (second jump uninteresting)) and (impossible second jump) 
    #          = (not E) and ((not E) and (not H))
    main = """
        NOT A J  # J true if A is a hole
        NOT B T  # T true if B is a hole
        OR T J   # J true if A or B is a hole
        NOT C T  # T true if C is a hole
        OR T J   # J is true if any of A,B,C is a hole

        NOT E T  # T true if E is a hole
        AND H T  # T true if E is a hole and H ground
        OR E T   # T true if E is ground, or (E is a hole and H ground)
        AND T J  # J is true if A,B,C is a hole and second jump is possible

        NOT D T  # T true if D is a hole
        NOT T T  # T true if D is ground <=> can jump
        AND T J  # J true if can jump, can do a second jump, and there is an incentive to jump
        RUN
    """

    part2 = springscript(intcode, main)
    return part1, part2

print(solve(intcode))