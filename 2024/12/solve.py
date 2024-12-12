import os.path
import collections

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def parse(data):
    garden_map = {}
    for y,line in enumerate(data.splitlines()):
        for x,c in enumerate(line):
            garden_map[(y,x)] = c
    return garden_map

def dfs(garden_map, coord, visited):
    queue = collections.deque([coord])
    visited.add(coord)
    area = 0
    perimeter = set()
    while queue:
        tile = queue.popleft()
        area += 1
        for n in ((-1,0),(1,0),(0,-1),(0,1)):
            nei = tile[0]+n[0], tile[1]+n[1]
            if garden_map.get(nei,None) == garden_map[tile]:
                if nei in visited:
                    continue
                queue.append(nei) 
                visited.add(nei)
            else:
                perimeter.add((tile, n))
    return area, perimeter

def part1(data):
    garden_map = parse(data)

    total_price = 0
    visited = set()
    for coord in garden_map.keys():
        if coord in visited:
            continue
        area, perimeter = dfs(garden_map, coord, visited)
        perimeter = len(perimeter)
        total_price += area*perimeter
    return total_price

test = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""
print(part1(test))
print(part1(data))

def count_sides(perimeter):
    sides = 0
    while perimeter:
        sides += 1
        (coord, side) = perimeter.pop()
        if side[1] == 0:
            d = ((0,-1),(0,1))
        else:
            d = ((-1,0),(1,0))
        for (dy,dx) in d:
            nc = coord[0]+dy, coord[1]+dx
            while (nc, side) in perimeter:
                perimeter.remove((nc,side))
                nc = nc[0]+dy, nc[1]+dx
    return sides

def part2(data):
    garden_map = parse(data)

    total_price = 0
    visited = set()
    for coord in garden_map.keys():
        if coord in visited:
            continue
        area, perimeter = dfs(garden_map, coord, visited)
        sides = count_sides(perimeter)
        total_price += area*sides
    return total_price

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))