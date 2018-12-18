data = open('input.txt').read()
import itertools

def print_area(area):
    print('\n'.join(''.join(line) for line in area))

def n8(y, x):
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dy != 0 or dx != 0:
                yield y+dy, x+dx

def count_tree_ly(area, y, x):
    ly_count = 0
    tree_count = 0
    for dy, dx in n8(y, x):
        if 0 <= dy < len(area) and 0 <= dx < len(area[dy]):
            if area[dy][dx] == '#':
                ly_count += 1
            elif area[dy][dx] == '|':
                tree_count += 1
    return tree_count, ly_count

def game_of_trees(input_data, debug=False):
    area = [list(line) for line in input_data.splitlines()]
    for _ in itertools.count():
        wooded_area = sum(1 for line in area for tile in line if tile in '|')
        ly_area = sum(1 for line in area for tile in line if tile in '#')
        yield (wooded_area*ly_area)

        new_area = [line[:] for line in area]
        for y, line in enumerate(area):
            for x, acre in enumerate(line):
                if acre == '.':
                    tree_count, _ = count_tree_ly(area, y, x)
                    if tree_count >= 3:
                        new_area[y][x] = '|'
                elif acre == '|':
                    _, ly_count = count_tree_ly(area, y, x)
                    if ly_count >= 3:
                        new_area[y][x] = '#'
                elif acre == '#':
                    tree_count, ly_count = count_tree_ly(area, y, x)
                    if ly_count > 0 and tree_count > 0:
                        pass
                    else:
                        new_area[y][x] = '.'
        area = new_area
        if debug:
            print_area(area)

def solve_part1(input_data):
    for t, resources in enumerate(game_of_trees(input_data)):
        if t == 10:
            return resources

print(solve_part1(""".#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|."""))

print(solve_part1(data))

def find_cycle(generator):
    last_seen = {}
    prev_cycle_size = 0
    cycle = []
    for t, value in enumerate(generator):
        if value in last_seen:
            cycle_size = t - last_seen[value]
            if cycle_size == prev_cycle_size:
                cycle.append(value)
                if len(cycle) == cycle_size:
                    # First value should be last value... or we just increment starting time by 0
                    cycle = cycle[-1:] + cycle[:-1]
                    return t-len(cycle), cycle
            else:
                cycle = [value]
            prev_cycle_size = cycle_size
        else:
            cycle = []
            prev_cycle_size = 0
        last_seen[value] = t

def find_value_at_cycling_generator(generator, large_t, includes_0_state=True, debug=False):
    cycle_start, cycle = find_cycle(generator)
    cycle_length = len(cycle)
    if not includes_0_state:
        cycle_start += 1
    d, m = divmod(large_t - cycle_start, cycle_length)
    if debug:
        print('Cycle start at', cycle_start, '. Cycle length is', cycle_length)
        print('Value at', cycle_start,'is',cycle[0])
        print('Value at', cycle_length*d + cycle_start,'is', cycle[0])
        print('Value at', cycle_length*d+m + cycle_start,'is', cycle[m])
    return cycle[m]

print(find_value_at_cycling_generator(game_of_trees(data), 1000000000))
