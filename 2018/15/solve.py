data = open('input.txt').read()

def find_targets(area, unit_type, y, x):
    t = []
    for d in ((-1, 0), (0, -1), (0, 1), (1, 0)):
        ny = y+d[0]
        nx = x+d[1]
        if area[ny][nx] == ('G' if unit_type == 'E' else 'E'):
            target = (area[ny][nx], ny, nx)
            t.append(target)

    return t

def search(area, move):
    unit_type, y, x = move
    queue = [(y, x, 0, None)]
    visited = set([(y, x)])
    possible_moves = []
    max_move_distance = 1e10
    while queue:
        (y, x, distance, first_move), queue = queue[0], queue[1:]

        # Terminate early (queue is always ordered by distance)
        if distance > max_move_distance:
            break

        for dy, dx in ((-1, 0), (0, -1), (0, 1), (1, 0)):
            ny = y+dy
            nx = x+dx
            if (ny,nx) in visited:
                continue
            visited.add((ny, nx))
            if area[ny][nx] == '.':
                queue.append((ny, nx, distance+1, first_move or (ny, nx)))
            elif area[ny][nx] == ('G' if unit_type == 'E' else 'E'):
                if first_move is None:
                    return 'fight', find_targets(area, unit_type, y, x)
                else:
                    possible_moves.append((y, x, distance, first_move))
                    max_move_distance = distance
    # Find first move in lexiographic order
    if possible_moves:
        return 'move', sorted(possible_moves)[0][3]
    return 'noop', None

def fight(area, attacker, targets, world_data):
    low_hp = 201
    low_hp_target = None
    for target_c in targets:
        target = world_data[target_c]
        if target['hp'] < low_hp:
            low_hp = target['hp']
            low_hp_target = target_c
    
    attacker = world_data[attacker]
    target = world_data[low_hp_target]
    target['hp'] -= attacker['atk']
    if target['hp'] <= 0:
        old_y = low_hp_target[1]
        old_x = low_hp_target[2]
        area[old_y] = area[old_y][:old_x] + '.' + area[old_y][old_x+1:]
        del world_data[low_hp_target]
        return low_hp_target[0]


def solve(data, elf_atk=3):
    area = data.splitlines()
    
    world_data = {}
    entity = 0
    for y, line in enumerate(area):
        for x, column in enumerate(line):
            if column == 'G':
                world_data[(column, y, x)] = {'atk': 3, 'hp': 200, 'id': entity}
                entity += 1
            elif column == 'E':
                world_data[(column, y, x)] = {'atk': elf_atk, 'hp': 200, 'id': entity}
                entity += 1
    t = 0
    while True:
        units = []
        for y, line in enumerate(area):
            for x, column in enumerate(line):
                if column == 'G' or column == 'E':
                    units.append(((column, y, x), world_data[(column, y, x)]['id']))

        for unit, entity in units:
            # Check also entity ID, it must match, otherwise this is some already moved unit
            # Fixes reddit edge case
            if unit not in world_data or world_data[unit]['id'] != entity:
                continue
            if all(unit[0] == some_unit[0] for some_unit in world_data.keys()):
                hp_sum = sum(o['hp'] for o in world_data.values())
                winning_side = unit[0]
                return t*hp_sum, winning_side

            action, action_data = search(area, unit)
            if action == 'move':
                unit_type = unit[0]
                old_y = unit[1]
                old_x = unit[2]
                area[old_y] = area[old_y][:old_x] + '.' + area[old_y][old_x+1:]
                
                new_y = action_data[0]
                new_x = action_data[1]
                area[new_y] = area[new_y][:new_x] + unit_type + area[new_y][new_x+1:]
                new_unit = (unit_type, new_y, new_x)

                world_data[new_unit] = world_data[unit]
                del world_data[unit]
                unit = new_unit

                targets = find_targets(area, unit_type, new_y, new_x)
                if targets:
                    action = 'fight'
                    action_data = targets
            if action == 'fight':
                casualty = fight(area, unit, action_data, world_data)
                if casualty == 'E' and elf_atk > 3:
                    return 0, 'G'
        t += 1


# Found edge case from Reddit thread where my code failed
print(solve("""####
##E#
#GG#
####""")[0], 67*200)

# Found edge case from Reddit thread where my code failed
print(solve("""#####
#GG##
#.###
#..E#
#.#G#
#.E##
#####
""")[0], 71*197)

print(solve("""#######   
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#   
#######""")[0], 27730)

print(solve("""#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######""")[0], 36334)
print(solve("""#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######""")[0], 39514)
print(solve("""#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######""")[0], 27755)
print(solve("""#######   
#.E...#
#.#..G#
#.###.#
#E#G#G# 
#...#G#
#######""")[0], 28944)
print(solve("""#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########""")[0], 18740)
print(solve(data)[0])

def solve2(data):
    for atk in range(4, 200):
        answer, winning_side = solve(data, atk)
        if 'E' == winning_side:
            return answer

print(solve2("""#######   
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#   
#######"""), 4988)
print(solve2("""#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######
"""), 31284)
print(solve2("""#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######"""), 3478)
print(solve2("""#######   
#.E...#
#.#..G#
#.###.#
#E#G#G# 
#...#G#
#######"""), 6474)
print(solve2("""#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########"""), 1140)

print(solve2(data))