import sys
data = sys.stdin.read()

count = 0
for line in data.splitlines():
    sides = [int(a) for a in line.split()]

    sides.sort()
    print(sides)

    if sides[0] + sides[1] > sides[2]:
        count += 1

print(count)


count = 0
lines = data.splitlines()
for i in range(0, len(lines), 3):
    sides1 = [int(a) for a in lines[i].split()]
    sides2 = [int(a) for a in lines[i+1].split()]
    sides3 = [int(a) for a in lines[i+2].split()]
    t1 = [sides1[0], sides2[0], sides3[0]]
    t2 = [sides1[1], sides2[1], sides3[1]]
    t3 = [sides1[2], sides2[2], sides3[2]]
    t1.sort()
    t2.sort()
    t3.sort()
    if t1[0] + t1[1] > t1[2]:
        count += 1
    if t2[0] + t2[1] > t2[2]:
        count += 1
    if t3[0] + t3[1] > t3[2]:
        count += 1

print(count)
