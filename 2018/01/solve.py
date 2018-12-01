data = open("input.txt").read().strip()

def solve(data):
    s = 0
    for line in data.splitlines():
        s += int(line)
    return s
print(solve(data))

def solve2(data):
    s = 0
    v = set()
    while True:
        for line in data.splitlines():
            s += int(line)
            if s in v:
                return s
            v.add(s)
print(solve2(data))