from io import TextIOBase
import os.path
import operator
from itertools import combinations, permutations
from functools import reduce, partial
from math import isfinite, prod, sqrt
from collections import Counter, defaultdict

INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

TEST=os.path.join(os.path.dirname(__file__), "test_input.txt")
with open(TEST) as f:
    test = f.read()

def parse_tiles(data):
    tiles={}
    monsters = data.split("\n\n")
    for monster in monsters:
        if not monster.strip():
            continue
        idline, *tile = monster.splitlines()
        id=int(idline.split()[1][:-1])
        tiles[id] = tile
    return tiles

# 0,0 0,1 0,2 0,3
# 1,0 1,1 1,2 1,3
# 2,0 2,1 2,2 2,3 
# 3,0 3,1 3,2 3,3
# --->
# 0,3 1,3 2,3 3,3
# 0,2 1,2 2,2 3,2
# 0,1 1,1 2,1 3,1
# 0,0 1,0 2,0 3,0

def rotate(tile):
    return ["".join(tile[x][len(tile)-y-1] for x in range(len(tile))) for y in range(len(tile))]

def flip(tile):
    return ["".join(tile[y][len(tile)-x-1] for x in range(len(tile))) for y in range(len(tile))]


def find_pairs(tiles):
    rotations = defaultdict(list)
    pairs = defaultdict(list)
    for id, tile in tiles.items():
        for _ in range(4):
            rotations[id].append(tile)
            tile = rotate(tile)
        tile = flip(tile)
        for _ in range(4):
            rotations[id].append(tile)
            tile = rotate(tile)

    for id1, id2 in combinations(tiles.keys(), 2):
        for i in range(4):
            for j in range(8):
                if rotations[id1][i][0] == rotations[id2][j][0]:
                    pairs[id1].append((i,j,id2))
                    pairs[id2].append((j,i,id1))
    return pairs, rotations

def find_corners(pairs):
    corners = []
    for id, pair in pairs.items():
        if len(pair) == 2:
            corners.append(id)
    return corners

def part1(data):
    tiles = parse_tiles(data)
    pairs, _ = find_pairs(tiles)
    return prod(find_corners(pairs))

print(part1(test))
print(part1(data))

def top(tile):
    return tile[0]

def bottom(tile):
    return tile[-1]

def left(tile):
    return "".join(l[0] for l in tile)

def right(tile):
    return "".join(l[-1] for l in tile)

def set(big_tile, tile, y, x):
    if not 0 <= y < 12:
        return
    if not 0 <= x < 12:
        return
    a=len(tile)-2
    for yy in range(a):
        by = y*a+yy
        for xx in range(a):
            bx = x*a+xx
            if not big_tile[by][bx] == "?":
                return
            v = tile[yy+1][xx+1]
            big_tile[by][bx] = v

def part2(data):
    tiles = parse_tiles(data)
    pairs, rotations = find_pairs(tiles)
    corners = find_corners(pairs)
    num_tiles = int(sqrt(len(tiles)))
    tile_len = (len(tiles[corners[0]])-2)*num_tiles
    big_tile = [['?' for x in range(tile_len)] for y in range(tile_len)]
    top_left = None
    for c in corners:
        has_right_left = False
        has_bottom_top = False
        tile = tiles[c]
        for _,_,o in pairs[c]:
            for other_tile in rotations[o]:
                if right(tile) == left(other_tile):
                    has_right_left = True
                if bottom(tile) == top(other_tile):
                    has_bottom_top = True
        if has_right_left and has_bottom_top:
            top_left = (c, tile)
    assert top_left is not None
    q = [(*top_left, 0, 0)]
    added = {top_left[0]}
    tile_map = {(0,0): top_left[1]}
    while q:
        id,tile,y,x = q.pop()
        set(big_tile, tile, y, x)
        for _,_,o in pairs[id]:
            if o in added:
                continue
            for other_tile in rotations[o]:
                if right(tile) == left(other_tile):
                    q.append((o,other_tile,y,x+1))
                    added.add(o)
                    tile_map[(y,x+1)] = other_tile
                if bottom(tile) == top(other_tile):
                    q.append((o,other_tile,y+1,x))
                    added.add(o)
                    tile_map[(y+1,x)] = other_tile
    assert all(c != "?" for r in big_tile for c in r)

    roughness = 0
    for _ in range(2):
        for _ in range(4):
            r = find_sea_monsters(big_tile)
            if r is not None:
                assert roughness == 0
                roughness = r
            big_tile = rotate(big_tile)
        big_tile = flip(big_tile)
    return roughness
    
def find_sea_monsters(area):
    monster = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """.splitlines()
    monster_high = len(monster)
    monster_width = len(monster[0])
    monster_coord = []
    for y in range(len(area)-monster_high):
        for x in range(len(area[0])-monster_width):
            not_a_monster = False
            water_roughness = 0
            for j, monster_line in enumerate(monster):
                for i, c in enumerate(monster_line):
                    if c == "#":
                        if area[y+j][x+i] != "#":
                            not_a_monster = True
            if not not_a_monster:
                monster_coord.append((y,x))
    monster_size = "".join(monster).count("#")
    water_roughness = "".join("".join(s) for s in area).count("#") - monster_size*len(monster_coord)
    return water_roughness if monster_coord else None


print(part2(test))
print(part2(data))

