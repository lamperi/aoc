import os.path
import collections
import re
import math
import time
import itertools
INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()


def solve(data):
    p1 = []
    p2 = []
    p = 1
    for line in data.splitlines():
        if not line:
            p = 2
            continue
        if ":" in line:
            continue
        if p == 1:
            p1.append(int(line))
        else:
            p2.append(int(line))
    
    while p1 and p2:
        a = p1.pop(0)
        b = p2.pop(0)
        if a > b:
            p1.append(a)
            p1.append(b)
        else:
            p2.append(b)
            p2.append(a)
    score = 0
    winning = p1 if p1 else p2
    for m, c in enumerate(reversed(winning)):
        score += (m+1)*c
    return score

print(solve(data))


def solve2(data):
    p1 = []
    p2 = []
    p = 1
    for line in data.splitlines():
        if not line:
            p = 2
            continue
        if ":" in line:
            continue
        if p == 1:
            p1.append(int(line))
        else:
            p2.append(int(line))
    p1_force_win = recursive_game(p1, p2)
    score = 0
    winning = p1 if p1 or p1_force_win else p2
    for m, c in enumerate(reversed(winning)):
        score += (m+1)*c
    return score

def recursive_game(p1, p2, g=1):
    previous_turns = set()
    while p1 and p2:
        p1s = tuple(p1)
        p2s = tuple(p2)
        if (p1s, p2s) in previous_turns:
            return True

        previous_turns.add((p1s, p2s))
        a = p1.pop(0)
        b = p2.pop(0)

        if a <= len(p1) and b <= len(p2):
            p1c = p1[:a]
            p2c = p2[:b]
            p1_force_win = recursive_game(p1c, p2c, g+1)
            p1_win = len(p1c) > 0 or p1_force_win     
        else:
            p1_win = a > b
        if p1_win:
            p1.append(a)
            p1.append(b)
        else:
            p2.append(b)
            p2.append(a)  
    return False

print(solve2("""Player 1:
43
19

Player 2:
2
29
14"""))
print(291, solve2("""Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""))
print(solve2(data))