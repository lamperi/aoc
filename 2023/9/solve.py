import os.path
from itertools import pairwise
from functools import reduce

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def parse(data):
    cases = []
    for line in data.splitlines():
        nums = [int(n) for n in line.split()]
        cases.append(nums)
    return cases

def differences(numbers):
    for nums in numbers:
        levels = [nums]
        level = nums
        while any(level) != 0:
            new_level = []
            for a,b in pairwise(level):
                new_level.append(b-a)
            levels.append(new_level)
            level = new_level
        yield levels

def solve_sum_of_next(numbers, oper):
    s = 0
    for levels in differences(numbers):
        inc = reduce(oper, reversed(levels), 0)
        s += inc
    return s

def part1(data):
    numbers = parse(data)
    return solve_sum_of_next(numbers, lambda inc, l: l[-1] + inc)

test = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""
print(part1(test))
print(part1(data))

def part2(data):
    numbers = parse(data)
    return solve_sum_of_next(numbers, lambda inc, l: l[0] - inc)

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))