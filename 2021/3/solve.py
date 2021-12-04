from io import TextIOBase
import os.path
import operator
from itertools import combinations, permutations
from functools import reduce, partial
from math import prod
from collections import Counter

INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

test="""00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""

def transpose_lines(data):
    tp=[]
    for n, line in enumerate(data.splitlines()):
        for i, c in enumerate(line):
            if n == 0:
                tp.append([c])
            else:
                tp[i].append(c)
    return tp

def part1(data):
    gamma=[]
    epsilon=[]
    for bb in transpose_lines(data):
        if bb.count("0") > bb.count("1"):
            gamma.append("0")
            epsilon.append("1")
        else:
            gamma.append("1")
            epsilon.append("0")
    gamma_rate=int("".join(gamma), 2)
    epsilon_rate=int("".join(epsilon), 2)
    return gamma_rate * epsilon_rate

print(part1(test), 198)
print(part1(data))

def part2(data):
    oxygen = data.splitlines()
    for i in range(0, 200):
        counts={"0": 0, "1": 0}
        for n in oxygen:
            counts[n[i]]+=1
        bit_criteria = "0" if counts["0"] > counts["1"] else "1"
        oxygen = [n for n in oxygen if n[i] == bit_criteria]
        if len(oxygen) == 1:
            break
    co2 = data.splitlines()
    for i in range(0, 200):
        counts={"0": 0, "1": 0}
        for n in co2:
            counts[n[i]]+=1
        bit_criteria = "0" if counts["0"] <= counts["1"] else "1"
        co2 = [n for n in co2 if n[i] == bit_criteria]
        if len(co2) == 1:
            break

    oxygen_rating=int(oxygen[0], 2)
    co2_rating=int(co2[0], 2)
    return oxygen_rating * co2_rating

print(part2(test), 230)
print(part2(data))

