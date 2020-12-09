import os.path
import collections
import re
import math
import itertools
INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

def solve(data, preamble_len=25):
    num = []
    for line in data.split("\n"):
        if not line:
            break
        n = int(line)
        num.append(n)
    preamble = num[:preamble_len]
    key = None
    for n in num[preamble_len:]:
        found = False
        for a,b in itertools.combinations(preamble, 2):
            if a+b == n:
                preamble.pop(0)
                preamble.append(n)
                found = True
                break
        if not found:
            key = n
            break
    for i, s in enumerate(num):
        j = i+1
        while s < key:
            s += num[j]
            j += 1
        if s == key:
            weakness = min(num[i:j]) + max(num[i:j])
            return key, weakness


print(solve("""35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576""", 5))

print(solve(data))
