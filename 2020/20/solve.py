import os.path
import collections
import re
import math
import itertools
INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()
INPUT=os.path.join(os.path.dirname(__file__), "test_input.txt")
with open(INPUT) as f:
    testdata = f.read()

def get_walls(tile_map):
    yield tile_map[0]
    right_wall = "".join(l[-1] for l in tile_map)
    yield right_wall
    yield tile_map[-1][::-1]
    left_wall = "".join(l[0] for l in tile_map)
    yield left_wall[::-1]

def transform(map, rot, flip):
    new_map = []
    for y, line in enumerate(map):
        new_line = []
        for x, _ in enumerate(line):
            yy = -y if flip else y
            xx = x
            for _ in range(rot):
                yy,xx = -xx,yy
            new_line.append(map[yy][xx])
        new_map.append("".join(new_line))
    return new_map

def to_painting(big_map, tiles):
    size = int(math.sqrt(len(tiles)))
    if True:
        for map_y in range(size):
            line = []
            for map_x in range(size):
                if (map_y,map_x) in big_map:
                    id, rot, flip = big_map[(map_y,map_x)]
                    line.append("{id} {rot} {f}".format(id=id, rot=rot, f=">" if flip else "<"))
                else:
                    line.append("xxxx y ?")
            #print(" ".join(line))
    full_map=[]
    for map_y in range(size):
        line = []
        for map_x in range(size):
            if (map_y,map_x) in big_map:
                id, rot, flip = big_map[(map_y,map_x)]
                tile_map = tiles[id]
                transformed = []
                for y in range(10):
                    transformed_line = []
                    for x in range(10):
                        if not flip:
                            yy = y
                            xx = x
                            for _ in range(rot):
                                yy, xx = 9-xx, yy
                        else:
                            yy = 9-y
                            xx = x
                            for _ in range(4-rot):
                                yy, xx = 9-xx, yy
                            
                        transformed_line.append(tile_map[yy][xx])
                    transformed.append("".join(transformed_line))
                line.append(transformed)
            else:
                assert False
        for yy in range(1,9):
            print_line = []
            for tile in line:
                print_line.append(tile[yy][1:-1])
            full_map.append("".join(print_line))
    #print("\n".join(full_map))
    return full_map

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
def get_wall_facing(dir, rot, flip):
    if not flip:
        return [0, 1, 2, 3][(dir - rot) % 4]
    else:
        return [2, 1, 0, 3][(dir - rot) % 4]

def get_rot(dir, wall_facing, flip):
    return ROT[(dir, wall_facing, flip)]

WALL_FACING = {}
ROT = {}
for dir in UP, RIGHT, DOWN, LEFT:
    for rot in (0, 1, 2, 3):
        for flip in False, True:
            facing = get_wall_facing(dir, rot, flip)
            WALL_FACING[(dir, rot, flip)] = facing
            ROT[(dir, facing, flip)] = rot
#print(WALL_FACING)
#print(ROT)

def solve(data):
    tiles_data = data.split("\n\n")
    tiles = {}
    for tile in tiles_data:
        if not tile.strip():
            continue
        lines = tile.splitlines()
        tile_id = lines[0].split()[1][:-1]
        tile_map = lines[1:]
        tiles[tile_id] = tile_map
    
    matches = collections.defaultdict(list)
    for tile_id, tile_map in tiles.items():
        walls = list(get_walls(tile_map))
        reverse_walls = [w[::-1] for w in walls]
        #reverse_walls = [reverse_walls[0], reverse_walls[3], reverse_walls[2], reverse_walls[1]]
        for friend_tile_id, friend_tile_map in tiles.items():
            if friend_tile_id <= tile_id:
                continue
            friend_walls = list(get_walls(friend_tile_map))
            for i, w in enumerate(walls):
                for j, fw in enumerate(friend_walls):
                    if w == fw:
                        matches[(tile_id, i)].append((True, friend_tile_id, j))
                        matches[(friend_tile_id, j)].append((True, tile_id, i))
            for i, w in enumerate(reverse_walls):
                for j, fw in enumerate(friend_walls):
                    if w == fw:
                        matches[(tile_id, i)].append((False, friend_tile_id, j))
                        matches[(friend_tile_id, j)].append((False, tile_id, i))
    by_wall = collections.defaultdict(set)
    for tile_id, w in matches.keys():
        by_wall[tile_id].add(w)
    corners = set(tile_id for tile_id, w in by_wall.items() if len(w) == 2)
    assert len(corners) == 4
    p = 1
    for c in corners:
        p *= int(c)
    part1 = p

    # Form image
    # i = 0,1,2,3 = up,right,down,left
    top_left = min(corners) if len(tiles) != 9 else "1951"
    big_map = {}
    big_map[(0,0)] = (top_left, (1-min(by_wall[top_left])) % 4, False)
    pieces = [(0,0)]
    used_pos = set(pieces)
    used_id = set([top_left])
    max_column = max_row = int(math.sqrt(len(tiles))) - 1
    while pieces:
        assert len(used_id) == len(used_pos)
        row, column = pieces.pop(0)
        prev_id, prev_rot, prev_flip = big_map[(row, column)]
        adj = []
        if column < max_column:
            adj.append(((row, column+1), RIGHT, LEFT))
        if row < max_row:
            adj.append(((row+1, column), DOWN, UP))
        if row > 0:
            adj.append(((row-1, column), UP, DOWN))
        if column > 0:
            adj.append(((row, column-1), LEFT, RIGHT))
        for next_pos, prev_facing, next_facing in adj:
            if next_pos in used_pos:
                continue
            next_wall_id = get_wall_facing(prev_facing, prev_rot, prev_flip)
            matching  = matches[(prev_id, next_wall_id)]
            matching = [m for m in matching if m[1] not in used_id]
            if len(matching) == 1:
                invert_flip, match_id, the_wall = matching[0]
                used_pos.add(next_pos)
                used_id.add(match_id)
                next_flip = not invert_flip if prev_flip else invert_flip
                next_rot = get_rot(next_facing, the_wall, next_flip)
                
                big_map[next_pos] = (match_id, next_rot, next_flip)
                pieces.append(next_pos)
            elif len(matching) > 1:
                assert False

        if len(tiles) == len(used_id):
            break

        if not pieces and False:
            assert False

    assert len(used_id) == len(used_pos) == len(tiles)
    mapp = to_painting(big_map, tiles)
    for rot in (0,1,2,3):
        for flip in (False, True):
            transformed_map = transform(mapp, rot, flip)
            roughness = find_sea_monsters(transformed_map)
            if roughness:
                part2 = roughness
    return part1, part2

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
    water_roughness = "".join(area).count("#") - monster_size*len(monster_coord)
    return water_roughness if monster_coord else None

print(solve(testdata))
print(solve(data))