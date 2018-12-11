
def make_grid(grid_serial):
    grid = [[0]*300 for i in range(300)]
    for i in range(300):
        for j in range(300):
            x = i+1
            y = j+1
            rack_id = x + 10
            power_level = (rack_id * y + grid_serial) * rack_id
            hundreds = int(power_level / 100) % 10
            power_level = hundreds - 5
            grid[j][i] = power_level
    return grid

def solve(grid_serial):
    grid = make_grid(grid_serial)
    max_level = 0
    max_coords = None
    for i in range(0, 298):
        for j in range(0, 298):
            s = 0
            for x in range(i, i+3):
                for y in range(j, j+3):
                    s += grid[y][x]
            if s > max_level:
                max_level = s
                max_coords = (i+1, j+1)
    return "{},{}".format(max_coords[0], max_coords[1])

print(solve(42), "21,61")
print(solve(7403))


def iterate(i, j):
    def iterate_size(size):
        for x in range(i, i+size):
            y = j+size-1
            yield x, y
        for y in range(j, j+size-1):
            x = i+size-1
            yield x, y

    max_size = min(i, j, 299-i, 299-j) + 2
    for size in range(1, max_size):
        yield size, iterate_size(size)


def solve2_fast(grid_serial):
    grid = make_grid(grid_serial)
    max_level = 0
    max_coords = None
    for i in range(0, 300):
        for j in range(0, 300):
            s = 0
            for size, coord_gen in iterate(i, j):
                for x, y in coord_gen:
                    s += grid[y][x]
                if s > max_level:
                    max_level = s
                    max_coords = (i+1, j+1, size)
    return "{},{},{}".format(max_coords[0], max_coords[1], max_coords[2])

print(solve2_fast(18), "90,269,16")
print(solve2_fast(42), "232,251,12")
print(solve2_fast(7403))

def solve2(grid_serial):
    grid = make_grid(grid_serial)
    max_level = 0
    max_coords = None
    for i in range(0, 300):
        for j in range(0, 300):
            max_size = min(i, j, 300-i, 300-j) + 1
            # heuristics to make it faster :(
            min_size = 8
            max_size = min(max_size, 20)
            for size in range(min_size, max_size):
                s = 0
                for x in range(i, i+size):
                    for y in range(j, j+size):
                        s += grid[y][x]
                if s > max_level:
                    max_level = s
                    max_coords = (i+1, j+1, size)
    return "{},{},{}".format(max_coords[0], max_coords[1], max_coords[2])

print(solve2(18), "90,269,16")
print(solve2(42), "232,251,12")
print(solve2(7403))