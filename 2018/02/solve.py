data = open("input.txt").read().strip()

from collections import Counter

def solve1(data):
    a = 0
    b = 0
    for line in data.splitlines():
        c = Counter(list(line))
        if 2 in c.values():
            a += 1
        if 3 in c.values():
            b += 1
    return a*b
print(solve1(data))

def solve2(data):
    words = data.splitlines()
    for w1 in words:
        for w2 in words:
            if w1 != w2:
                d = sum(1 for x,y in zip(w1, w2) if x != y)
                if d == 1:
                    res = "".join(x for x,y in zip(w1, w2) if x == y)
                    return res

print(solve2(data))
