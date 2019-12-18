with open("input.txt") as f:
    data = f.read().strip()

import string
import heapq

def dir_to_pos(dir):
    return {1: (-1, 0), 2: (1, 0), 3: (0, 1), 4: (0, -1)}[dir]

def pos_sum(x,y):
    return x[0] + y[0], x[1] + y[1]

def keys_with_blocks(pos, area, missing_keys, locked_doors):
    visited = {pos: 0}
    blocking = {pos: set()}
    blocking_key = {pos: set()}
    l = [pos]
    keys = {}
    while l:
        p = l[0]
        l = l[1:]
        for y,x in (pos_sum(p, dir_to_pos(i)) for i in (1,2,3,4)):
            if (y,x) in visited:
                continue
            tile = area.get((y,x))
            if tile != "#":
                l.append((y,x))
                visited[(y,x)] = visited[p] + 1
                blocking[(y,x)] = blocking[p].copy()
                blocking_key[(y,x)] = blocking_key[p].copy()
                if tile in locked_doors:
                    blocking[(y,x)].add(tile.lower())
                if tile in missing_keys:
                    keys[tile] = {'dist': visited[(y,x)], 'blocking': blocking[(y,x)], 'blocking_key': blocking_key[(y,x)].copy()}
                    if len(keys) == len(missing_keys):
                        return sorted(keys.items(), key=lambda t: t[1]['dist'])
                    blocking_key[(y,x)].add(tile)
    return keys.items()

def key_bfs_precalc(entrances, dist_map, keys, doors):
    init_conf = (frozenset(entrances), frozenset(keys.keys()))
    best_conf = {init_conf: 0}
    heap = [(0, init_conf)]

    while heap:
        di, (pp, ke) = heapq.heappop(heap)
        if len(ke) == 0:
            return di
        for p in pp:
            #print(dist_map.keys())
            for k, r in ((x, dist_map[p][x]) for x in ke if x in dist_map[p]):
                if len(r['blocking'] & ke) > 0:
                    continue
                if len(r['blocking_key'] & ke) > 0:
                    continue
                new_ke = frozenset(ke - {k})
                new_di = di + r['dist']
                conf = (((pp - {p}) | {keys[k]}), new_ke)
                prev_di = best_conf.get(conf, None)
                if prev_di is not None and prev_di < new_di:
                    continue
                else:
                    best_conf[conf] = new_di
                    if prev_di is not None:
                        for i, tup in enumerate(heap):
                            if tup[1] == conf:
                                new_item = (new_di, tup[1])
                                heap[i] = new_item
                                # Instead of: heapq.heapify(heap)
                                # https://stackoverflow.com/questions/10162679/python-delete-element-from-heap
                                # Private API for heapq:
                                heap[i] = heap[-1]
                                heap.pop()
                                if i < len(heap):
                                    heapq._siftup(heap, i)
                                    heapq._siftdown(heap, 0, i)
                                heapq.heappush(heap, new_item)
                                break
                        else:
                            print("Failed to replace a previously known state from heap.\nCurrent best {}, new best {}".format(best_conf[conf], new_di))
                            assert False
                        continue
                heapq.heappush(heap, (new_di, conf))


def transform_map(data):
    area = {}
    entrance = None
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            area[(y,x)] = c
            if c == "@":
                entrance = (y,x)
    area[entrance] = '#'
    for p2 in (pos_sum(entrance, dir_to_pos(i)) for i in (1,2,3,4)):
        area[p2] = '#'
    for p2 in (pos_sum(entrance, (y,x)) for y,x in ((-1,1), (-1,-1), (1,-1), (1,1))):
        area[p2] = '@'
    data = []
    for y in range(0, 1+max(y for y,x in area.keys())):
        l = []
        for x in range(0, 1+max(x for y,x in area.keys())):
            l.append(area[y,x])
        data.append("".join(l))
    data = "\n".join(data)
    #print(data)
    return data

def solve(data):
    area = {}
    entrances = []
    keys = {}
    doors = {}
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            area[(y,x)] = c
            if c == "@":
                entrances.append((y,x))
            elif c in string.ascii_lowercase:
                keys[c] = (y,x)
            elif c in string.ascii_uppercase:
                doors[c] = (y,x)
    # Precalculate all distances PLAYING there are no doors.
    DIST_AND_BLOCK = {e: {} for e in entrances}
    for entrance in entrances:
        for k, r in keys_with_blocks(entrance, area, keys.keys(), doors.keys()):
            DIST_AND_BLOCK[entrance][k] = r
    for key, pos in keys.items():
        DIST_AND_BLOCK[pos] = {}
        for k, r in keys_with_blocks(pos, area, keys.keys() - set(key), doors.keys()):
            DIST_AND_BLOCK[pos][k] = r
    return key_bfs_precalc(entrances, DIST_AND_BLOCK, keys, doors.keys())

print(solve("""#########
#b.A.@.a#
#########"""), 8)

print(solve("""########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################"""), 86)

print(solve("""########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################"""), 132)

if False:  # Slow
    print(solve("""#################
    #i.G..c...e..H.p#
    ########.########
    #j.A..b...f..D.o#
    ########@########
    #k.E..a...g..B.n#
    ########.########
    #l.F..d...h..C.m#
    #################"""), 136)

print(solve("""########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################"""), 81)

print("PART1", solve(data))

print(solve(transform_map("""#######
#a.#Cd#
##...##
##.@.##
##...##
#cB#Ab#
#######""")), 8)

print("PART2", solve(transform_map(data)))