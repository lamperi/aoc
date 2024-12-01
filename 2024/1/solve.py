import os.path

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()



aa = []
bb = []
for line in data.splitlines():
    a,b = line.split()
    a = int(a)
    b = int(b)
    aa.append(a)
    bb.append(b)
    
aa.sort()
bb.sort()

s = 0
for a,b in zip(aa,bb):
    d = abs(a-b)
    s += d
    
print(s)


s = 0
for a in aa:
    n = 0
    for b in bb:
        if b == a:
            n += 1
    s += a * n
    
print(s)