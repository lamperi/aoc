with open("input.txt") as f:
    data = f.read()

def dir_to_pos(dir):
    return {1: (-1, 0), 2: (1, 0), 3: (0, 1), 4: (0, -1)}[dir]

def pos_sum(x,y):
    return x[0] + y[0], x[1] + y[1]

def biodiversity(area):
    b = 0
    for (y,x), c in area:
        if c == "#":
            b += 2**(y*5 + x)
    return b

def solve(data):
    area = {}
    seen_areas = set()
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            area[(y,x)] = c

    while True:
        a = frozenset(area.items())
        if a in seen_areas:
            return biodiversity(a)
        seen_areas.add(a)

        b = {}
        for pos, c in area.items():
            bugs = 0
            for new_pos in (pos_sum(pos, dir_to_pos(i)) for i in (1,2,3,4)):
                if area.get(new_pos, ".") == "#":
                    bugs += 1
            if c == "#" and bugs != 1:
                b[pos] = "."
            elif c == "." and (bugs == 1 or bugs == 2):
                b[pos] = "#"
            else:
                b[pos] = c
        area = b


print(solve("""....#
#..#.
#..##
..#..
#...."""))

print(solve(data))

def get_adjacent(pos):
    y,x,l = pos
    # up
    if y == 3 and x == 2:
        for xx in range(5):
            yield (4,xx,l+1)
    elif y == 0:
        yield (1,2,l-1)
    else:
        yield (y-1,x,l)
    # left
    if y == 2 and x == 3:
        for yy in range(5):
            yield (yy,4,l+1)
    elif x == 0:
        yield (2,1,l-1)
    else:
        yield (y,x-1,l)
    # down
    if y == 1 and x == 2:
        for xx in range(5):
            yield (0,xx,l+1)
    elif y == 4:
        yield (3,2,l-1)
    else:
        yield (y+1,x,l)
    # right
    if y == 2 and x == 1:
        for yy in range(5):
            yield (yy,0,l+1)
    elif x == 4:
        yield (2,3,l-1)
    else:
        yield (y,x+1,l)

def print_area(area):
    min_depth = min(d for (y,x,d) in area.keys())
    max_depth = max(d for (y,x,d) in area.keys())
    s = []
    for d in range(min_depth, max_depth+1):
        s.append("Depth {}:\n".format(d))
        for y in range(5):
            for x in range(5):
                s.append(area[(y,x,d)])
            s.append("\n")
        s.append("\n")
    print("".join(s))

def solve2(data, minutes):
    area = {}
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            area[(y,x,0)] = c
    area[(2,2,0)] = "?"

    for m in range(minutes):
        # extend current search

        for y in range(5):
            for x in range(5):
                c = "?" if y == 2 and x == 2 else "."
                area[(y,x,-m-1)] = c
                area[(y,x,m+1)] = c
 
        new_area = {}
        for pos, c in area.items():
            bugs = 0
            for new_pos in get_adjacent(pos):
                assert new_pos != "?"
                if area.get(new_pos, ".") == "#":
                    bugs += 1
            if c == "#" and bugs != 1:
                new_area[pos] = "."
            elif c == "." and (bugs == 1 or bugs == 2):
                new_area[pos] = "#"
            else:
                new_area[pos] = c
        area = new_area

    if minutes < 15:
        print("Minute",m)
        print_area(area)

    return sum(1 for c in area.values() if c == "#")

print(solve2("""....#
#..#.
#.?##
..#..
#....""", 10))

print(solve2(data, 200))