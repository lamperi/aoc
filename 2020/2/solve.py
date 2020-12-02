import os.path
INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

import re
r = re.compile(r"(\d+)-(\d+) (.): (.+)")
s1, s2 = 0, 0
for line in data.splitlines():
    m = r.match(line)
    l=int(m[1])
    h=int(m[2])
    assert m is not None
    if l <= m[4].count(m[3]) <= h:
        s1+=1
    if m[4][l-1] == m[3] and m[4][h-1] != m[3] or m[4][l-1] != m[3] and m[4][h-1] == m[3]:
        s2+=1
print(s1, s2)