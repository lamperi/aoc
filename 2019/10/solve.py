with open("input.txt") as f:
    data = f.read().strip()
data = data.splitlines()

def view(m, I, J):
    b = set()
    for dy in range(-len(m), len(m)):
        for dx in range(-len(m), len(m)):
            if dy == 0 and dx == 0:
                continue
            found = False
            i, j = I, J
            while True:
                i, j = i+dy, j+dx
                if i < 0 or j < 0 or i >= len(m) or j >= len(m[i]):
                    break
                if m[i][j] == '#':
                    if not found:
                        found = True
                    else:
                        b.add((i,j))
    total = sum(sum(1 for c in line if c == '#') for line in m)
    
    #print(total, miss, len(b), I, J)
    return total - len(b) - 1

def solve(map):
    m = 0
    mc = None
    for i, line in enumerate(map):
        for j, c in enumerate(line):
            if c == '#':
                a = view(map, i, j)
                if a > m:
                    m = a
                    mc = i,j 
    #print(mc)
    return m


print(solve(""".#..#
.....
#####
....#
...##""".splitlines()))

print(solve("""......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####""".splitlines()))

print(solve("""#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.""".splitlines()))

print(solve(""".#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..""".splitlines()))


print(solve(""".#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##""".splitlines()))

print(solve(data))

from math import atan2, gcd

def yield_angle(I, J, m):
    all_diffs = [(y-I, x-J) for y, line in enumerate(m) for x, _ in enumerate(line) if gcd(y-I,x-J) == 1]
    all_diffs = sorted((-atan2(dx, dy), dy, dx) for dy, dx in all_diffs)
    while True:
        for _,dy,dx in all_diffs:
            yield dy,dx

def vaporize(m, I, J, N):
    b = set()
    for dy, dx in yield_angle(I, J, m):
        i, j = I, J
        while True:
            i, j = i+dy, j+dx
            if i < 0 or j < 0 or i >= len(m) or j >= len(m[i]):
                break
            if m[i][j] == '#' and m[i][j] not in b:
                b.add((i,j))
                if len(b) == N:
                    return (i+100*j)
                break
print(vaporize(""".#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....X...###..
..#.#.....#....##""".splitlines(), 3, 8, 9))

print(vaporize(data, 16, 8, 200))