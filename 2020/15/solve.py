import os.path
import collections
import re
import math
import itertools
INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

def solve(data, target):
    num = [int(i) for i in data.strip().split(",")]
    last = {}
    previous = {}
    for i, n in enumerate(num):
        last[n] = i
    previous_num = num[-1]
    len_num = len(num)
    del num
    while len_num < target:
        add = None
        if previous_num in previous.keys():
            add = last[previous_num] - previous[previous_num]
        else:
            add = 0
        previous_num = add
        if add in last.keys():
            previous[add] = last[add]
        last[add] = len_num
        len_num += 1
    return previous_num

solve1 = lambda data: solve(data, 2020)
solve2 = lambda data: solve(data, 30000000)

print(solve1("""0,3,6"""), 436)
print(solve1("""1,3,2"""), 1)
print(solve1("""2,1,3"""), 10)
print(solve1(data))

print(solve2("""0,3,6"""), 175594)
print(solve2("""1,3,2"""), 2578)
print(solve2("""2,1,3"""), 3544142)
print(solve2(data))