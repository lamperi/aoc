with open("input.txt") as f:
    data = f.read()

import string

def dir_to_pos(dir):
    return {1: (-1, 0), 2: (1, 0), 3: (0, 1), 4: (0, -1)}[dir]

def pos_sum(x,y):
    return x[0] + y[0], x[1] + y[1]

def solve(data):
    area = {}
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            area[(y,x)] = c
    max_y = max(y for (y,x) in area.keys())
    max_x = max(x for (y,x) in area.keys())
    portals = {}
    for y in range(max_y+1):
        for x in range(max_x+1):
            if area[(y,x)] in string.ascii_uppercase:
                if area.get((y+1,x), "?") in string.ascii_uppercase:
                    portal = area[(y,x)] + area[(y+1,x)]
                    if area.get((y+2,x), "?") == ".":
                        portals[(y+2,x)] = portal
                    else:
                        portals[(y-1,x)] = portal
                elif area.get((y,x+1), "?") in string.ascii_uppercase:
                    portal = area[(y,x)] + area[(y,x+1)]
                    if area.get((y,x+2), "?") == ".":
                        portals[(y,x+2)] = portal
                    else:
                        portals[(y,x-1)] = portal
    
    for coord, portal in portals.items():
        if portal == "AA":
            start = coord
        elif portal == "ZZ":
            end = coord
    del portals[start]
    del portals[end]
    visited = {start: 0}
    l = [start]
    while l:
        pos = l[0]
        l = l[1:]
        for new_pos in (pos_sum(pos, dir_to_pos(i)) for i in (1,2,3,4)):
            if new_pos == end:
                return visited[pos] + 1
            elif new_pos in visited:
                continue
            elif area.get(new_pos, "") == ".":
                l.append(new_pos)
                visited[new_pos] = visited[pos] + 1
            elif area.get(new_pos, "?") in string.ascii_uppercase and pos in portals:
                portal = portals[pos]
                pair_portal_pos = [pp for pp, p in portals.items() if p == portal and pp != pos][0]
                l.append(pair_portal_pos)
                visited[pair_portal_pos] = visited[pos] + 1
                
def solve2(data):
    area = {}
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            area[(y,x)] = c
    max_y = max(y for (y,x) in area.keys())
    max_x = max(x for (y,x) in area.keys())
    portals = {}
    for y in range(max_y+1):
        for x in range(max_x+1):
            if area[(y,x)] in string.ascii_uppercase:
                if area.get((y+1,x), "?") in string.ascii_uppercase:
                    portal = area[(y,x)] + area[(y+1,x)]
                    if area.get((y+2,x), "?") == ".":
                        portals[(y+2,x)] = portal
                    else:
                        portals[(y-1,x)] = portal
                elif area.get((y,x+1), "?") in string.ascii_uppercase:
                    portal = area[(y,x)] + area[(y,x+1)]
                    if area.get((y,x+2), "?") == ".":
                        portals[(y,x+2)] = portal
                    else:
                        portals[(y,x-1)] = portal
    
    for coord, portal in portals.items():
        if portal == "AA":
            start = coord
        elif portal == "ZZ":
            end = coord
    # These are not actual portals!
    del portals[start]
    del portals[end]
    visited = {(0,start): 0}
    l = [(0,start)]
    while l:
        level, pos = state = l[0]
        l = l[1:]
        for new_pos in (pos_sum(pos, dir_to_pos(i)) for i in (1,2,3,4)):
            if new_pos == end and level == 0:
                return visited[(level,pos)] + 1
            elif pos in portals and area.get(new_pos, "?") in string.ascii_uppercase:
                if new_pos[0] < 5 or (max_y-new_pos[0]) < 5 or new_pos[1] < 5 or (max_x-new_pos[1]) < 5:
                    new_level = level-1
                else:
                    new_level = level+1
                if new_level < 0: # Dead path
                    continue
                portal = portals[pos]
                pair_portal_pos = [pp for pp, p in portals.items() if p == portal and pp != pos][0]
                new_state = (new_level, pair_portal_pos)
                if new_state in visited:
                    continue
                l.append(new_state)
                visited[new_state] = visited[state] + 1
            elif area.get(new_pos, "") == ".":
                new_state = (level, new_pos)
                if new_state in visited:
                    continue
                l.append(new_state)
                visited[new_state] = visited[state] + 1

print(solve("""                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P               """))

print(solve("""         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       """))

print(solve(data))

print(solve2("""             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                     """))

print(solve2(data))