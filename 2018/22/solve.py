data = open('input.txt').read()
from heapq import heappop, heappush

def geo_index(cave, y, x, target_y, target_x):
    if y == x == 0:
        return 0
    if y == 0:
        return x * 16807
    if x == 0:
        return y * 48271
    if y == target_y and x == target_x:
        return 0
    return cave[y-1][x] * cave[y][x-1]

def erosion_level(geo_index, depth):
    return ((geo_index + depth) % 20183)

def risk(erosion_level):
    return erosion_level % 3

class Tool:
    Torch = 1
    Gear = 2
    Neither = 0

def actions(cave, y, x, tool):
    for dy, dx in ((-1, 0), (0, -1), (1, 0), (0, 1)):
        ny, nx = dy+y, dx+x
        if ny >= 0 and nx >= 0 and ny < len(cave) and nx < len(cave[ny]):
            nrisk = risk(cave[ny][nx])
            if nrisk != tool:
                yield ny, nx, tool, 1
    for ntool in (0,1,2):
        if ntool != tool and ntool != risk(cave[y][x]):
            yield y, x, ntool, 7

def print_route(cave, y, x, tool, parents):
    path = dict()
    while True:
        path[(y,x)] = str(tool)
        y, x, tool = parents[(y,x,tool)]
        if y is None:
            break
    
    for y, line in enumerate(cave[:15]):
        c = []
        for x, tile in enumerate(line[:15]):
            if (y,x) in path:
                c.append(path[(y,x)])
            else:
                c.append({0: '.', 1: '=', 2: '|'}[tile % 3])
        print(''.join(c))

def solve_cave(cave, target_y, target_x):
    queue = [(0, 0, 0, Tool.Torch, None, None, None)]
    seen = {}
    while queue:
        cost, y, x, tool, py, px, ptool = heappop(queue)
        if (y, x, tool) in seen:
            continue
        seen[(y,x, tool)]  = (py, px, ptool)
        if y == target_y and x == target_x and tool == Tool.Torch:
            #print_route(cave, y, x, Tool.Torch, seen)
            return cost
        for ny, nx, move_tool, move_cost in actions(cave, y, x, tool):
            heappush(queue, (cost+move_cost, ny, nx, move_tool, y, x, tool))

def solve(depth, target_x, target_y):
    padd = 50
    cave = [[0]*(padd+target_x) for _ in range(target_y+padd)]
    risk_level = 0
    for y in range(target_y+padd):
        for x in range(target_x+padd):
            geoi = geo_index(cave, y, x, target_y, target_x)
            ero = erosion_level(geoi, depth)
            cave[y][x] = ero
            if y <= target_y and x <= target_x:
                risk_level += risk(ero)
    return risk_level, solve_cave(cave, target_y, target_x)

print(solve(510, 10, 10))
print(solve(11817, 9, 751))
