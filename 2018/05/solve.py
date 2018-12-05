data = open("input.txt").read().strip()

import re
from collections import Counter

def solve1(data):
    prevData = None
    while data != prevData:
        prevData = data
        for a,b in zip(data, data[1:]):
            if (a != b and a == b.lower()) or (a != b and a.lower() == b):
                data = data.replace(a+b, "")
                break

    return len(data)

print(solve1("""dabAcCaCBAcCcaDA"""))

print(solve1(data))

def solve2(data):
    min_len = len(data)
    min_chr = None
    for c in 'abcdefghijklmnopqrstubwxyz':
        d = data.replace(c, "").replace(c.upper(), "")
        l = solve1(d)
        if l < min_len:
            min_len = l
            min_chr = c
    return min_len

print(solve2("""dabAcCaCBAcCcaDA"""))

print(solve2(data))
