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

test="""target area: x=20..30, y=-10..-5"""

def part12(data):
    l = data.split()
    x=l[2]
    y=l[3]
    min_x, max_x = list(map(int, x.split("=")[1].split(",")[0].split("..")))
    min_y, max_y = list(map(int, y.split("=")[1].split("..")))
    highest_y=0
    matches=set()
    # vy is limited so that:
    # - smaller one would make shot go past on first step
    # - larger one would make shot go past on first step after it comes back from high point
    # vx in limited so that larger one would make shot go past on first step
    for vy in range(min_y,-min_y):
        for vx in range(max_x+1):
            s=(0,0)
            v=(vy,vx)
            ymax=0
            hit=False
            for t in range(500000):
                s = (s[0]+v[0], s[1]+v[1])
                ymax = max((ymax, s[0]))
                v=(v[0]-1, max(0, v[1]-1))
                if min_x <= s[1] <= max_x and min_y <= s[0] <= max_y:
                    hit=True
                    break
                elif s[0] < min_y or s[1] > max_x:
                    break
            if hit:
                matches.add((vy,vx))
                highest_y = max((highest_y, ymax))
    return f"{highest_y} {len(matches)}"
 

print(part12(test))
print(part12(data))


