with open("input.txt") as file:
    data = file.read()

m = [-1, 0, 1]
def neight(grid, x, y):
    for a in m:
        for b in m:
            if a == b == 0:
                continue
            xx = x+a
            yy = y+b
            if 0 <= xx < len(grid) and 0 <= yy < len(grid[xx]):
                yield grid[xx][yy]

def neight_on(grid, x, y):
    return sum(1 for c in neight(grid, x, y) if c == '#')

def update_corners(grid):
    new_grid = []
    for x in range(len(grid)):
        l = []
        for y in range(len(grid[x])):
            if x in (0, len(grid)-1) and y in (0, len(grid[x])-1):
                l.append('#') 
            else: # pass
                l.append(grid[x][y])
        new_grid.append("".join(l))
    return new_grid

def update(grid):
    new_grid = []
    for x in range(len(grid)):
        l = []
        for y in range(len(grid[x])):
            on_count = neight_on(grid,x,y)
            if x in (0, len(grid)-1) and y in (0, len(grid[x])-1):
                l.append('#') 
            elif grid[x][y] == '#': # on
                l.append('#' if on_count in (2,3) else '.')
            else: # pass
                l.append('#' if on_count == 3 else '.')
        new_grid.append("".join(l))
    return new_grid
     
# TEST           
grid = """.#.#.#
...##.
#....#
..#...
#.#..#
####..""".splitlines()

for i in range(4):
    grid = update(grid)
    print("\n".join(grid) + "\n")   
    
# PART 1
grid = data.splitlines()
for i in range(100):
    grid = update(grid)
    
s = sum(1 for row in grid for c in row if c == '#')
print(s)


# TEST 2
grid = """.#.#.#
...##.
#....#
..#...
#.#..#
####..""".splitlines()
grid = update_corners(grid)

for i in range(5):
    grid = update_corners(update(grid))
    print("\n".join(grid) + "\n")   
    
# PART 1
grid = data.splitlines()
grid = update_corners(grid)
for i in range(100):
    grid = update_corners(update(grid))
    
s = sum(1 for row in grid for c in row if c == '#')
print(s)