import os.path
from collections import Counter

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def part1(data):
    robots = []
    for line in data.splitlines():
        pos, vel = line.split()
        x,y = pos.split("=")[1].split(",")
        x = int(x)
        y = int(y)
        vx,vy = vel.split("=")[1].split(",")
        vx = int(vx)
        vy = int(vy)
        robots.append((x,y,vx,vy))
    
    if len(robots) < 20:
        w = 11
        h = 7
    else:
        w = 101
        h = 103
    for i in range(100):
        new_robots = []
        for r in robots:
            x,y,vx,vy = r
            nx = (x + vx) % w
            ny = (y + vy) % h
            new_robots.append((nx,ny,vx,vy))
        robots = new_robots
    
    q = [0,0,0,0]
    for r in robots:
        x,y,vx,vy = r
        mx = (w-1)/2
        my = (h-1)/2
        if x < mx and y < my:
            q[0] += 1
        elif x < mx and y > my:
            q[1] += 1
        elif x > mx and y < my:
            q[2] += 1
        elif x > mx and y > my:
            q[3] += 1
    
    return q[0]*q[1]*q[2]*q[3]

test = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""
print(part1(test))
print(part1(data))

def part2(data):
    robots = []
    for line in data.splitlines():
        pos, vel = line.split()
        x,y = pos.split("=")[1].split(",")
        x = int(x)
        y = int(y)
        vx,vy = vel.split("=")[1].split(",")
        vx = int(vx)
        vy = int(vy)
        robots.append((x,y,vx,vy))
    
    if len(robots) < 20:
        w = 11
        h = 7
    else:
        w = 101
        h = 103
    t = 0
    while True:
        new_robots = []
        for r in robots:
            x,y,vx,vy = r
            nx = (x + vx) % w
            ny = (y + vy) % h
            new_robots.append((nx,ny,vx,vy))
        robots = new_robots
        t += 1

        occupied = frozenset([(x,y) for x,y,_,_ in robots])
        visited = set()
        for start in occupied:
            if start in visited:
                continue
            queue = [start]
            visited.add(start)
            current_path = 0
            while queue:
                current_path += 1
                x,y = queue.pop(0)
                for n in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
                    if n in visited:
                        continue
                    if n in occupied:
                        queue.append(n)
                        visited.add(n)
            if current_path > 200:
                #print_all(robots, w, h, t)
                return t

def print_all(robots, w, h, t):
    s = [["."]*w for _ in range(h)]
    for (x,y,_,_) in robots:
        s[y][x] = "#"
    print(f"----- Turns:{t} -----")
    print("\n".join(''.join(a) for a in s))
    print("")

# Override test for part 2.
# test = """ """

#print(part2(test))
print(part2(data))