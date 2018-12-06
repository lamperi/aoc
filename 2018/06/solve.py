data = open("input.txt").read().strip()

import re
import string
from collections import Counter

L = string.ascii_lowercase + "!#¤%&/())=?^|<>1234567890"

def neight(x, y, n):
    a = x-n
    b = y
    for i in range(n):
        yield(a,b)
        a += 1
        b += 1
    for i in range(n):
        yield(a,b)
        a += 1
        b -= 1
    for i in range(n):
        yield(a,b)
        a -= 1
        b -= 1
    for i in range(n):
        yield(a,b)
        a -= 1
        b += 1

# The actual code I used for part 1 .... super slow to code but faster to execute
def solve1(data):
    c = []
    for line in data.splitlines():
        x, y = map(int, line.split(", "))
        c.append((x, y))
    min_x = min(x for x,y in c)
    max_x = max(x for x,y in c)
    min_y = min(y for x,y in c)
    max_y = max(y for x,y in c)
    
    area = [["." for x in range(min_x, max_x+1)] for y in range(min_y, max_y+1)]
    i = 1
    for n, (x, y) in enumerate(c):
        l = L[n]
        area[y-min_y][x-min_x] = l

    while True:
        visited = {}
        for n, (x, y) in enumerate(c):
            l = L[n]
            for xn, yn in neight(x, y, i):
                if min_x <= xn <= max_x and min_y <= yn <= max_y:
                    if area[yn-min_y][xn-min_x] == '.':
                        if (xn,yn) not in visited:
                            visited[(xn,yn)] = l
                        else:
                            visited[(xn,yn)] = '-'
        
        for coords, label in visited.items():
            area[coords[1]-min_y][coords[0]-min_x] = label
        #print("\n".join("".join(a) for a in area))
        #print()
        if any(l != '-' for l in visited.values()):
            i += 1
        else:
            break

    #print("\n".join("".join(a) for a in area))

    counter = Counter()
    for n, (x, y) in enumerate(c):
        l = L[n]
        i = 1
        area_size = 1
        while True:
            any_found = False
            for xn, yn in neight(x, y, i):
                if min_x <= xn <= max_x and min_y <= yn <= max_y:
                    if area[yn-min_y][xn-min_x] == l:
                        area_size += 1
                        any_found = True
                        if xn == min_x or xn == max_x or yn == min_y or yn == max_y:
                            # infinite
                            any_found = False
                            area_size = 0
                            break
            if any_found:
                i += 1
            else:
                break
        counter[l] = area_size

    return counter.most_common(1)[0][1]

print(solve1("""1, 1
1, 6
8, 3
3, 4
5, 5
8, 9"""))
print(solve1(data))

def md(x,y,x2,y2):
    return abs(x-x2) + abs(y-y2)

# Afterthough for part 1 - just brute force it
def solve1_bf(data):
    c = []
    for line in data.splitlines():
        x, y = map(int, line.split(", "))
        c.append((x, y))
    min_x = min(x for x,y in c)
    max_x = max(x for x,y in c)
    min_y = min(y for x,y in c)
    max_y = max(y for x,y in c)

    counter = Counter()
    # set of labels that are infinite
    lim = set()
    for x in range(min_x, max_x+1):
        for y in range(min_y, max_y+1):
            min_d = max_y+max_x
            min_l = None
            for l, (xc, yc) in enumerate(c):
                d = md(x,y,xc,yc)
                if d < min_d:
                    min_d = d
                    min_l = l
                elif d == min_d:
                    min_l = None
            if min_l is not None:
                counter[min_l] += 1
                # Detect infinity
                if x == min_x or x == max_x or y == min_y or y == max_y:
                    lim.add(min_l)
    # Just remove values for infinite areas to find most common faster
    for l in lim:
        counter[l] = 0
    return counter.most_common(1)[0][1]

print(solve1_bf("""1, 1
1, 6
8, 3
3, 4
5, 5
8, 9"""))
print(solve1_bf(data))


def solve2(data, n):
    c = []
    for line in data.splitlines():
        x, y = map(int, line.split(", "))
        c.append((x, y))
    min_x = min(x for x,y in c)
    max_x = max(x for x,y in c)
    min_y = min(y for x,y in c)
    max_y = max(y for x,y in c)

    r = 0
    for x in range(min_x, max_x+1):
        for y in range(min_y, max_y+1):
            if sum(md(x,y,xc,yc) for xc, yc in c) < n:
                r += 1
    return r

print(solve2("""1, 1
1, 6
8, 3
3, 4
5, 5
8, 9""", 32))
print(solve2(data, 10000))
