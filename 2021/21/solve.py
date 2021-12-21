import operator
import os.path
import re
from collections import Counter, defaultdict
from functools import partial, reduce
from heapq import heappop, heappush
from io import TextIOBase
from itertools import combinations, pairwise, permutations
from math import isfinite, prod

INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

test="""Player 1 starting position: 4
Player 2 starting position: 8"""

def part1(data):
    p = [int(w[-1]) for w in data.splitlines()]
    i = 0
    scores = [0,0]
    while True:
        for player in (0,1):
            throw = (i+3) + (i+1) + (i+2)
            p[player] = (p[player] + throw) % 10
            scores[player] += p[player] if p[player] !=0 else 10
            i += 3
            if scores[player] >= 1000:
                return(scores[1-player]*i)

print(part1(test))
print(part1(data))

def part2(data):
    THROWS = [(3,1),(4,3),(5,6),(6,7),(7,6),(8,3),(9,1)]
    """
    Should have generated with this instead of by hand:

        throws = defaultdict(int)
        for i in (1,2,3):
            for j in (1,2,3):
                for k in (1,2,3):
                    throws[i+j+k] += 1
        print(list(sorted(throws.items())))
        assert list(sorted(throws.items())) == THROWS
    """

    states = defaultdict(int)
    states[(tuple(int(w[-1]) for w in data.splitlines()), (0, 0), 0)] = 1
    winner = [0,0]
    while states:
        for player in (0,1):
            new_states = defaultdict(int)
            for throw,count in THROWS:
                for (pos, scores, throw_count), times in states.items():
                    pos = list(pos)
                    scores = list(scores)
                    pos[player] = (pos[player] + throw) % 10
                    scores[player] += pos[player] if pos[player] != 0 else 10
                    pos = tuple(pos)
                    scores = tuple(scores)
                    if scores[player] >= 21:
                        winner[player] += times*count
                        continue
                    new_states[(pos, scores, throw_count + 3)] += times * count
            states = new_states
    return max(winner)

print(part2(test))
print(part2(data))

