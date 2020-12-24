import os.path
import collections
import re
import math
import time
import itertools
from timeit import default_timer as timer
INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

def solve(data):
    # e, se, sw, w, nw, and ne
    tiles = []
    for line in data.splitlines():
        i = 0
        path = []
        while i < len(line):
            if line[i] in ("e", "w"):
                path.append(line[i])
                i += 1
            else:
                path.append(line[i:i+2])
                i += 2
        tiles.append(path)
    # coordinates: 0,0
    neighbors = {"w": (0, -2), "e": (0, 2), "se": (1, 1), "sw": (1, -1), "ne": (-1, 1), "nw": (-1, -1)}
    blacks = set()
    for path in tiles:
        c = 0, 0
        for step in path:
            diff = neighbors[step]
            c = c[0] + diff[0], c[1] + diff[1]
        if c not in blacks:
            blacks.add(c)
        else:
            blacks.remove(c)
    s = len(blacks)

    for _ in range(100):
        white_with_black_neigh = {}
        black_with_black_neigh = {}
        for coord in blacks:
            if coord not in black_with_black_neigh:
                black_with_black_neigh[coord] = 0
            for diff in neighbors.values():
                c = coord[0] + diff[0], coord[1] + diff[1]
                if c not in blacks:
                    white_with_black_neigh[c] = white_with_black_neigh.get(c, 0) + 1
                else:
                    black_with_black_neigh[c] = black_with_black_neigh.get(c, 0) + 1
        for coord, count in black_with_black_neigh.items():
            if count == 0 or count > 2:
                blacks.remove(coord)
        for coord, count in white_with_black_neigh.items():
            if count == 2:
                blacks.add(coord)

    s2 = len(blacks)
    return s, s2

print(solve("""sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""))
print(solve(data))