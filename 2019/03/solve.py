with open("input.txt") as f:
    data = f.read().strip()

def manh(p):
    return abs(p[0]) + abs(p[1])

def solve(inst1, inst2):
    v = set()
    p = (0, 0)
    v.add(p)
    intersects = set()
    steps1 = {}
    steps2 = {}
    step = 0
    for i in inst1:
        d, n = i[0], int(i[1:])
        if d == "D":
            D = (0, -1)
        elif d == "U":
            D = (0, 1)
        elif d == "L":
            D = (-1, 0)
        elif d == "R":
            D = (1, 0)
        for i in range(n):
            p = p[0]+D[0], p[1]+D[1]
            step += 1
            steps1[p] = step
            v.add(p)
    p = (0, 0)
    step = 0
    for i in inst2:
        d, n = i[0], int(i[1:])
        if d == "D":
            D = (0, -1)
        elif d == "U":
            D = (0, 1)
        elif d == "L":
            D = (-1, 0)
        elif d == "R":
            D = (1, 0)
        for i in range(n):
            p = p[0]+D[0], p[1]+D[1]
            step += 1
            steps2[p] = step
            if p in v:
                intersects.add(p)
    return min(manh(p) for p in intersects), min(steps1[p]+steps2[p] for p in intersects)
        

print(solve("R8,U5,L5,D3".split(","), "U7,R6,D4,L4".split(",")))
print(solve("R75,D30,R83,U83,L12,D49,R71,U7,L72".split(","),
"U62,R66,U55,R34,D71,R55,D58,R83".split(",")))

lines=data.splitlines()
inst1 = [a for a in lines[0].split(",")]
inst2 = [a for a in lines[1].split(",")]


print(solve(inst1, inst2))