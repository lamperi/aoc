import os.path
import collections
import re
import math
import itertools
INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

def solve(data):
    num = [0]
    for line in data.split("\n"):
        if not line:
            break
        n = int(line)
        num.append(n)
    num = sorted(num)
    x = 0
    y = 1
    for a,b in zip(num, num[1:]):
        if b-a == 1:
            x+=1
        elif b-a == 3:
            y+=1
    s1 = (x*y)

    i = len(num)-2
    ways = {}
    ways[num[-1]] = 1
    while i >= 0:
         v = num[i]
         ways[v] = ways.get(v+1, 0) + ways.get(v+2, 0) + ways.get(v+3, 0)
         i -= 1
    s2 = ways[0]
    return s1, s2


print(solve("""16
10
15
5
1
11
7
19
6
12
4"""))

print(solve("""28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""))

print(solve(data))
