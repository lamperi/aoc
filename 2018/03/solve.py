data = open("input.txt").read().strip()

def parse_line(line):
    # #1181 @ 549,663: 10x18
    a = line.split(" @ ")
    b = a[1].split(": ")
    c = b[0].split(",")
    d = b[1].split("x")
    x = int(c[0])
    y = int(c[1])
    w = int(d[0])
    h = int(d[1])
    return x, y, w, h

def solve1(data):
    S=1000
    grid = [[0 for j in range(S)] for i in range(S)]
    for line in data.splitlines():
        # #1181 @ 549,663: 10x18
        x, y, w, h = parse_line(line)
        for a in range(x, x+w):
            for b in range(y, y+h):
                grid[b][a] += 1
    s = sum(1 for i in grid for j in i if j > 1)
    return s
print(solve1("""#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2"""))

print(solve1(data))

def solve2(data):
    S=1000
    grid = [[0 for j in range(S)] for i in range(S)]
    for line in data.splitlines():
        # #1181 @ 549,663: 10x18
        x, y, w, h = parse_line(line)
        for a in range(x, x+w):
            for b in range(y, y+h):
                grid[b][a] += 1
    
    for line in data.splitlines():
        # #1181 @ 549,663: 10x18
        x, y, w, h = parse_line(line)
        all = True
        for a in range(x, x+w):
            for b in range(y, y+h):
                if grid[b][a] != 1:
                    all = False
        if all:
            return line.split(" @ ")[0].split("#")[1]
print(solve2("""#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2"""))

print(solve2(data))