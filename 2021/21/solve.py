import itertools
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
    p = [int(w[-1])-1 for w in data.splitlines()]
    scores = [0,0]
    throws = 0
    while True:
        for player in (0,1):
            throw = 3*throws + 6
            throws += 3
            p[player] = (p[player] + throw) % 10
            scores[player] += p[player] + 1
            if scores[player] >= 1000:
                return(scores[1-player]*throws)
                

print(part1(test))
print(part1(data))

"""
Should have generated with this instead of by hand:

    throws = defaultdict(int)
    for i in (1,2,3):
        for j in (1,2,3):
            for k in (1,2,3):
                throws[i+j+k] += 1
    assert list(sorted(throws.items())) == THROWS
"""
THROWS = [(3,1),(4,3),(5,6),(6,7),(7,6),(8,3),(9,1)]

def simulate_multiverse(states, player):
    wins = 0
    new_states = defaultdict(int)
    for throw,count in THROWS:
        for (pos, score), times in states.items():
            new_pos = (pos[player] + throw) % 10
            new_score = score[player] + new_pos + 1
            if new_score >= 21:
                wins += times*count
                continue
            # Create new tuples by slicing - as immutables cannot directly change tuple
            pos = pos[:player] + (new_pos,) + pos[player+1:]
            score = score[:player] + (new_score,) + score[player+1:]
            new_states[(pos, score)] += times * count
    return new_states, wins

def part2(data):
    pos = tuple(int(w[-1])-1 for w in data.splitlines())
    states = {
        (pos, (0, 0)): 1,
    }
    winner = [0,0]
    while states:
        for player in (0,1):
            states, wins = simulate_multiverse(states, player)
            winner[player] += wins
    return max(winner)

print(part2(test))
print(part2(data))

