import os.path

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def part1(data):
    tile_map, moves = data.split("\n\n")
    
    tiles = {}
    start = None
    for y, line in enumerate(tile_map.splitlines()):
        for x, c in enumerate(line):
            if c in '#O':
                tiles[(y,x)] = c
            elif c == "@":
                start = (y,x)
    
    move_to_dy = {'v': 1, '^': -1, '<': 0, '>': 0}
    move_to_dx = {'v': 0, '^': 0, '<': -1, '>': 1}
    ry,rx = start
    for move in moves:
        if move == '\n':
            continue
        dy = move_to_dy[move]
        dx = move_to_dx[move]
        next_tile = tiles.get((ry+dy, rx+dx), None)
        if next_tile is None:
            ry = ry+dy
            rx = rx+dx
        elif next_tile == 'O':
            oy = ry+dy
            ox = rx+dx
            while True:
                o_tile = tiles.get((oy,ox), None)
                if o_tile is None:
                    ry = ry+dy
                    rx = rx+dx
                    del tiles[(ry,rx)]
                    tiles[(oy,ox)] = 'O'
                    break
                elif o_tile == '#':
                    break
                else:
                    assert o_tile == 'O'
                oy = oy+dy
                ox = ox+dx
        else:
            assert next_tile == '#'
    
    s = 0
    for (y,x), c in tiles.items():
        if c == 'O':
            #print(y,x,100*y+x)
            s += y*100 + x
    return s

test2 = """##########
#.O.O.OOO#
#........#
#OO......#
#OO@.....#
#O#.....O#
#O.....OO#
#O.....OO#
#OO....OO#
##########

>"""

test = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""
assert 10092 == part1(test)
print(part1(data))

def part2(data):
    tile_map, moves = data.split("\n\n")
    
    LEFT = 0
    RIGHT = 1
    
    tiles = {}
    boxes = {}
    start = None
    for y, line in enumerate(tile_map.splitlines()):
        for x, c in enumerate(line):
            if c == '#':
                tiles[(y,2*x)] = '#'
                tiles[(y,2*x+1)] = '#'
            elif c == 'O':
                boxes[(y,2*x)] = LEFT
                boxes[(y,2*x+1)] = RIGHT
            elif c == "@":
                start = (y,2*x)

    move_to_dy = {'v': 1, '^': -1, '<': 0, '>': 0}
    move_to_dx = {'v': 0, '^': 0, '<': -1, '>': 1}
    ry,rx = start
    for move in moves:
        if move == '\n':
            continue
        print_warehouse(tiles, boxes, (ry,rx))
        dy = move_to_dy[move]
        dx = move_to_dx[move]
        next_tile = tiles.get((ry+dy, rx+dx), None)
        if (ry+dy, rx+dx) in boxes:
            if dy == 0:
                # Moving left.
                moves = []
                oy = ry+dy
                ox = rx+dx
                while True:
                    if tiles.get((oy,ox), None) == '#':
                        break
                    elif boxes.get((oy, ox), None) == RIGHT:
                        if dx == -1:
                            moves.append((oy,ox))
                            moves.append((oy,ox-1))
                        else:
                            moves.append((oy,ox-1))
                            moves.append((oy,ox))
                        oy = oy+dy
                        ox = ox+dx
                    elif boxes.get((oy, ox), None) == LEFT:
                        oy = oy+dy
                        ox = ox+dx
                    else:
                        assert (oy,ox) not in boxes and (oy,ox) not in tiles
                        ry = ry+dy
                        rx = rx+dx
                        #print(moves)
                        for move in reversed(moves):
                            move_to = move[0]+dy, move[1]+dx
                            #print(f"{move} --> {move_to}")
                            assert move_to not in boxes, f"{move} --> {move_to} in {boxes}"
                            boxes[move_to] = boxes[move]
                            del boxes[move]
                        break
            elif dx == 0:
                # Moving up or down.
                moves = []
                moving = True
                colliding_tiles = set([(ry+dy, rx+dx)])
                while moving:
                    new_colliding_tiles = set()
                    for tile in colliding_tiles:
                        if tiles.get(tile, None) == '#':
                            moving = False
                            break
                        elif boxes.get(tile, None) == RIGHT:
                            left_tile = tile[0], tile[1]-1
                            new_colliding_tiles.add(left_tile)
                            new_colliding_tiles.add(tile)
                        elif boxes.get(tile, None) == LEFT:
                            right_tile = tile[0], tile[1]+1
                            new_colliding_tiles.add(tile)
                            new_colliding_tiles.add(right_tile)
                    moves.extend(new_colliding_tiles)
                    colliding_tiles = set(((y+dy,x+dx) for y,x in new_colliding_tiles))
                    if moving and not colliding_tiles:
                        ry = ry+dy
                        rx = rx+dx
                        #print(moves)
                        for move in reversed(moves):
                            move_to = move[0]+dy, move[1]+dx
                            #print(f"{move} --> {move_to}")
                            assert move_to not in boxes
                            boxes[move_to] = boxes[move]
                            del boxes[move]
                        moving = False
        elif next_tile is None:
            ry = ry+dy
            rx = rx+dx
    print_warehouse(tiles, boxes, (ry,rx))
    s = 0
    for (y,x), c in boxes.items():
        if c == LEFT:
            #print(y,x,100*y+x)
            s += y*100 + x
    return s

def print_warehouse(tiles, boxes, robot):
    return  # Remove me to debug.
    min_y = min(y for y,_ in tiles.keys())
    max_y = max(y for y,_ in tiles.keys())
    min_x = min(x for _,x in tiles.keys())
    max_x = max(x for _,x in tiles.keys())
    
    graphic = []
    for y in range(min_y, max_y + 1):
        line = []
        graphic.append(line)
        for x in range(min_x, max_x + 1):
            if (y,x) in tiles:
                line.append('#')
            elif (y,x) == robot:
                line.append('@')
            elif (y,x) in boxes:
                line.append('[]'[boxes[(y,x)]])
            else:
                line.append('.')
    print('\n'.join(''.join(line) for line in graphic))

assert 9021 == part2(test)
print(part2(data))