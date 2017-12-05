import sys
data = open("input.txt").read().strip()

def func(data):
    pos = 0
    inst = [int(line) for line in data.splitlines()]
    steps = 0
    while True:
        next = pos + inst[pos]
        inst[pos] += 1
        pos = next
        steps += 1
        if pos < 0 or pos >= len(inst):
            break 
    return steps

print(func(data))


def func(data):
    pos = 0
    inst = [int(line) for line in data.splitlines()]
    steps = 0
    while True:
        next = pos + inst[pos]
        if inst[pos] >= 3:
            inst[pos] -= 1
        else:
            inst[pos] += 1
        pos = next
        steps += 1
        if pos < 0 or pos >= len(inst):
            break 
    return steps

print(func(data))
