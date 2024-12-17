import os.path
from collections import defaultdict
from functools import reduce
from itertools import combinations

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def part1(data):
    registers,program = data.split("\n\n")
    reg = {}
    for register in registers.splitlines():
        _, name, value = register.split()
        reg[name[:-1]] = int(value)
    program = [int(inst) for inst in program.split()[1].split(",")]
    out =  run_program(reg, program)
    return ",".join(str(v) for v in out)

def run_program(reg, program):
    def combo(v):
        match v:
            case 0 | 1 | 2 | 3:
                return v
            case 4:
                return reg['A']
            case 5:
                return reg['B']
            case 6:
                return reg['C']
            case _:
                assert False
    
    inst_ptr = 0
    out = []
    while inst_ptr < len(program):
        inst = program[inst_ptr]
        arg = program[inst_ptr+1]
        match inst:
            case 0: # adv
                num = reg['A']
                den = 2**combo(arg)
                reg['A'] = num // den
            case 1:  # bxl
                reg['B'] = reg['B'] ^ arg
            case 2:  # bst
                reg['B'] = combo(arg) % 8
            case 3:  # jnz
                if reg['A'] != 0:
                    inst_ptr = arg
                    continue
            case 4:  # bxc
                reg['B'] = reg['B'] ^ reg['C']
            case 5:  # out
                out.append(combo(arg) % 8)
            case 6:  # bdv
                num = reg['A']
                den = 2**combo(arg)
                reg['B'] = num // den
            case 7:  # cdv
                num = reg['A']
                den = 2**combo(arg)
                reg['C'] = num // den
        inst_ptr += 2
    return out

test = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""
assert "4,6,3,5,6,3,5,2,1,0" == part1(test)
print(part1(data))

def part2_pre_process(data):
    registers,program = data.split("\n\n")
    reg = {}
    for register in registers.splitlines():
        _, name, value = register.split()
        reg[name[:-1]] = int(value)
    program = [int(inst) for inst in program.split()[1].split(",")]
    
    reg = {'A': 117440, 'B': 0, 'C': 0}
    out = run_program(reg, program)
    return out == program

def part2(data):
    _registers, program = data.split("\n\n")
    program = [int(inst) for inst in program.split()[1].split(",")]
    want = tuple(program)
    # A must be between 35184372088832 (1 << 45) inclusive and 281474976710656 exclusive (1 << 48)
    # Through brute forcing numbers that have many correct digits in the output:
    # the following bit ranges are always the same:
    # I believe this is specific to my input and doesn't apply to others.
    BITS_1_TO_16  = 0b0011110000001111
    BITS_33_TO_46 = 0b10110101011101
    # So let's brute force the rest of the ranges.
    candidates = []
    for bits_17_to_32 in range(1<<16):
        for bits_47_to_48 in range(1<<2):
            v = combine(bits_47_to_48, BITS_33_TO_46, bits_17_to_32, BITS_1_TO_16)
            p = run_program({'A': v, 'B': 0, 'C': 0}, program)
            if tuple(p) == want:
                candidates.append(v)
    return min(candidates)

def combine(u, x, y, z):
    return (u << 14 << 16 << 16) | (x << 16 << 16) | (y << 16) | (z)

print(part2(data))