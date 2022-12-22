import os.path
from operator import sub

FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(FILE) as f:
    INPUT = f.read()

TEST = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""


def solve(data):
    map, path = data.split("\n\n")
    map = map.splitlines()

    x = 0
    y = 0
    face = 1+0j # x,y
    for x, c in enumerate(map[0]):
        if c == ".":
            break
    
    path = path.replace("L", " L ").replace("R", " R ")
    path = path.split()
    for i, comp in enumerate(path):
        if comp == "L":
            face *= -1j
        elif comp == "R":
            face *= 1j
        else:
            l = int(comp)
            for _ in range(l):
                xn = int(x + face.real)
                yn = int(y + face.imag)
                if not (0 <= yn < len(map) and 0 <= xn < len(map[yn])) or map[yn][xn] == " ":
                    # out of bounds
                    if xn > x:
                        # wrap to left
                        for xn, c in enumerate(map[yn]):
                            if c in ("#", "."):
                                break
                    elif xn < x:
                        for xn_, c in enumerate(map[yn]):
                            if c in ("#", "."):
                                xn = xn_
                    elif yn > y:
                        for yn, row in enumerate(map):
                            if row[xn] in ("#", "."):
                                break
                    elif yn < y:
                        for yn_, row in enumerate(map):
                            if 0 <= xn < len(row) and row[xn] in ("#", "."):
                                yn = yn_
                    else:
                        assert False
                if map[yn][xn] == "#":
                    break
                elif map[yn][xn] == ".":
                    x = xn
                    y = yn

    return score(x,y,face)

def create_adjacent_cells(L, map):
    """
TEST:
        1111
        1111
        1111
        1111
222233334444
222233334444
222233334444
222233334444
        55556666
        55556666
        55556666
        55556666

INPUT:
    11112222
    11112222
    11112222
    11112222
    3333
    3333
    3333
    3333
44445555
44445555
44445555
44445555
6666
6666
6666
6666
    """
    mapping = {}
    if L == 4:
        return False
    elif L == 50:
        # Side 1111
        for y in range(1, 51):
            mapping[(50, y, -1)] = [(1, 151 - y, 1)]
            mapping[(101, y, 1)] = [(101, y, 1)]
        assert len(mapping) == 100
        for x in range(51, 101):
            mapping[(x, 0, -1j)] = [(1, x+100, 1)]
            mapping[(x, 51, 1j)] = [(x, 51, 1j)]
        assert len(mapping) == 200
        # Side 2222
        for y in range(1, 51):
            mapping[(100, y, -1)] = [(100, y, -1)]
            mapping[(151, y, 1)] = [(100, 151 - y, -1)]
        for x in range(101, 151):
            mapping[(x, 0, -1j)] = [(x-100, 200, -1j)]
            mapping[(x, 51, 1j)] = [(100, x-50, -1)]
        assert len(mapping) == 400
        # Side 3333
        for y in range(51, 101):
            mapping[(50, y, -1)] = [(y-50, 101, 1j)]
            mapping[(101, y, 1)] = [(y+50, 50, -1j)]
        for x in range(51, 101):
            mapping[(x, 50, -1j)] = [(x, 50, -1j)]
            mapping[(x, 101, 1j)] = [(x, 101, 1j)]
        assert len(mapping) == 600
        # Side 4444
        for y in range(101, 151):
            mapping[(0, y, -1)] = [(51, 151 - y, 1)]
            mapping[(51, y, 1)] = [(51, y, 1)]
        for x in range(1, 51):
            mapping[(x, 100, -1j)] = [(51, x + 50, 1)]
            mapping[(x, 151, 1j)] = [(x, 151, 1j)]
        assert len(mapping) == 800
        # Side 5555
        for y in range(101, 151):
            mapping[(50, y, -1)] = [(50, y, -1)]
            mapping[(101, y, 1)] = [(150, 151 - y, -1)]
        for x in range(51, 101):
            mapping[(x, 100, -1j)] = [(x, 100, -1j)]
            mapping[(x, 151, 1j)] = [(50, x + 100, -1)]
        assert len(mapping) == 1000
        # Side 6666
        for y in range(151, 201):
            mapping[(0, y, -1)] = [(y - 100, 1, 1j)]
            mapping[(51, y, 1)] = [(y - 100, 150, -1j)]
        for x in range(1, 51):
            mapping[(x, 150, -1j)] = [(x, 150, -1j)]
            mapping[(x, 201, 1j)] = [(x + 100, 1, 1j)]
        assert len(mapping) == 1200
    
    # Offset by one due to using 0 based indexing during search.
    new_mapping = {}
    for (x1,y1,d1), [(x2,y2,d2)] in mapping.items():
        new_mapping[(x1-1, y1-1, d1)] = (x2-1, y2-1, d2)
        #print((x1,y1,d1), [(x2,y2,d2)])
    mapping = new_mapping
    assert len(mapping) == 1200
    return mapping

def solve2(data, L=4):
    map, path = data.split("\n\n")
    map = map.splitlines()

    mapping = create_adjacent_cells(L, map)

    # Find start
    x = 0
    y = 0
    face = 1+0j # x,y
    for x, c in enumerate(map[0]):
        if c == ".":
            break

    path = path.replace("L", " L ").replace("R", " R ")
    path = path.split()
    for i, comp in enumerate(path):
        if comp == "L":
            face *= -1j
        elif comp == "R":
            face *= 1j
        else:
            l = int(comp)
            for _ in range(l):
                xn = int(x + face.real)
                yn = int(y + face.imag)
                fn = face
                if not (0 <= yn < len(map) and 0 <= xn < len(map[yn])) or map[yn][xn] == " ":
                    xn, yn, fn = mapping[(xn, yn, fn)]
                if map[yn][xn] == "#":
                    break
                elif map[yn][xn] == ".":
                    x = xn
                    y = yn
                    face = fn
                else:
                    assert False, (xn, yn)
    return score(x,y,face)

def score(x,y,face):
    row = y+1
    column = x+1
    if face == 1+0j:
        facing = 0
    elif face == 0+1j:
        facing = 1
    elif face == -1+0j:
        facing = 2
    elif face == 0-1j:
        facing = 3
    else:
        assert False
    return 1000*row + 4*column + facing

print(solve(TEST))
print(solve(INPUT))

# Doesn't work as the graph is hardcoded for my input.
#print(solve2(TEST, 4))
print(solve2(INPUT, 50))