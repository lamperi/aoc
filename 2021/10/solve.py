from io import TextIOBase
import os.path
import operator
from itertools import combinations, permutations
from functools import reduce, partial
from math import isfinite, prod
from collections import Counter

INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

test="""[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""


syntax_pairs={
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}
syntax_error_code={
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}
def part1(data):
    ec=0  # total syntax error code
    for line in data.splitlines():
        s = []
        for c in line:
            if c in "([{<":
                s.append(c)
            elif c in ")]}>":
                if len(s) == 0 or c != syntax_pairs[s.pop()]:
                    ec += syntax_error_code[c]
                    break
    return ec

print(part1(test))
print(part1(data))

points_to_complete={
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4,
}
def part2(data):
    scores=[]
    for line in data.splitlines():
        s = []
        bad = False
        for c in line:
            if c in "([{<":
                s.append(c)
            elif c in ")]}>":
                if len(s) == 0 or c != syntax_pairs[s.pop()]:
                    bad=True
                    break
        if bad:
            continue
        line_score = 0
        while s:
            c = s.pop()
            line_score *= 5
            line_score += points_to_complete[c]
        scores.append(line_score)
    scores.sort()
    return scores[len(scores)//2]

print(part2(test))
print(part2(data))

