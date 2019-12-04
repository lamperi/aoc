with open("input.txt") as f:
    data = f.read().strip()

from collections import Counter

a,b = data.split("-")
a,b = int(a), int(b)

c1, c2 = 0, 0
for i in range(a, b+1):
    co = Counter(str(i))
    if str(i) == "".join(sorted(str(i))):
        if any(v >= 2 for k,v in co.items()):
            c1 += 1
        if any(v == 2 for k,v in co.items()):
            c2 += 1
print(c1, c2)