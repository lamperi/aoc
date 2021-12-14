from io import TextIOBase
import os.path
import operator
from itertools import combinations, permutations
from functools import reduce, partial
from math import isfinite, prod
from collections import Counter, defaultdict
import re

INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

test="""NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

def part1(data):
    tmpl, pairs = data.split("\n\n")
    pair_insertions = {}
    for line in pairs.splitlines():
        a,b = line.split(" -> ")
        pair_insertions[(a[0], a[1])] = b

    # Naiive approach: just generate the string.
    for t in range(10):
        n = []
        for a,b in zip(tmpl, tmpl[1:]):
            i = pair_insertions.get((a,b), None)
            n.append(a)
            if i is not None:
                n.append(i)
        n.append(tmpl[-1])
        tmpl = n
    c = Counter(tmpl)
    mc = c.most_common()
    return mc[0][1] - mc[-1][1]

print(part1(test))
print(part1(data))

def part2(data):
    tmpl, pairs = data.split("\n\n")
    pair_insertions = {}
    for line in pairs.splitlines():
        a,b = line.split(" -> ")
        pair_insertions[(a[0], a[1])] = b

    # Optimized approach: deconstrct the string into pairs.
    pairs = defaultdict(int)
    for a,b in zip(tmpl, tmpl[1:]):
        pairs[(a,b)] += 1
    for t in range(40):
        new_pairs = defaultdict(int)
        for pair,count in pairs.items():
            i = pair_insertions.get(pair, None)
            if i is not None:
                new_pairs[(pair[0], i)] += count
                new_pairs[(i, pair[1])] += count
            else:
                new_pairs[(pair[0], pair[1])] += count
        pairs = new_pairs
    # Only count the first item of pair.
    counter=Counter()
    for (a,b),c in pairs.items():
        counter[a] += c
    # The last character of the string is uncounter at this stage (because it never started anything).
    counter[tmpl[-1]] += 1
    mc = counter.most_common()
    return mc[0][1] - mc[-1][1]

print(part2(test))
print(part2(data))

