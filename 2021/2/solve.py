from io import TextIOBase
import os.path
import operator
from itertools import combinations, permutations
from functools import reduce, partial
from math import prod

INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

test="""forward 5
down 5
forward 8
up 3
down 8
forward 2"""


def part1(data):
    # part 1
    pos=(0,0)
    for line in data.splitlines():
        rule, arg = line.split()
        arg = int(arg)
        if rule == "forward":
            pos = pos[0] + arg, pos[1]
        if rule == "down":
            pos = pos[0], pos[1] + arg
        if rule == "up":
            pos = pos[0], pos[1] - arg
    print(abs(pos[1]*pos[0]))

part1(test)
part1(data)

def part2(data):
    #part 2
    pos=(0,0)
    aim=0
    for line in data.splitlines():
        rule, arg = line.split()
        arg = int(arg)
        if rule == "forward":
            pos = pos[0] + arg, pos[1] + aim*arg
        if rule == "down":
            aim += arg
        if rule == "up":
            aim -= arg
    print(abs(pos[1]*pos[0]))

part2(test)
part2(data)