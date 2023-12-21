import os.path
import math

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def part1(data, steps=64):
    area = data.splitlines()
    tiles = {}
    for y, line in enumerate(area):
        for x, c in enumerate(line):
            tiles[(y,x)] = c
            if c == "S":
                start = (y,x)

    locations = set([start])
    for step in range(steps):
        new_locations = set()
        for loc in locations:
            for adj in ((1,0), (-1,0), (0,1), (0,-1)):
                new_loc = loc[0] + adj[0], loc[1] + adj[1]
                t = tiles.get(new_loc, "#") 
                if t == "S" or t == ".":
                    new_locations.add(new_loc)
        locations = new_locations
    return len(locations)

test = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""
print(part1(test, 6))
print(part1(data))

def part2(data, steps=26501365):
    area = data.splitlines()
    tiles = {}
    for y, line in enumerate(area):
        for x, c in enumerate(line):
            if c == "S":
                start = (y,x)
                c = "."
            tiles[(y,x)] = c
            
    height = len(area)
    width = len(area[0])

    locations = set([start])

    first_ever = {}
    
    size_per_loc = {}
    
    loaded = False
    if width > 100:
        try: 
            import pickle
            with open("locations.pickle", "rb") as f:
                locations, size_per_loc, first_ever, verify, data_steps = pickle.load(f)
                loaded = True
                if data_steps != steps:
                    verify = False
        except:
            pass

    if not loaded:
        verify = True
        for step in range(steps):
            
            current_seen = {}
            for l in locations:
                i, y = divmod(l[0], height)
                j, x = divmod(l[1], width)
                if (i,j) not in current_seen:
                    current_seen[(i,j)] = set()
                current_seen[(i,j)].add((y,x))

            current_seen = {k: frozenset(s) for k, s in current_seen.items()}
            for k, s in current_seen.items():
                if k not in size_per_loc:
                    size_per_loc[k] = [len(s)]
                else:
                    l = size_per_loc[k]
                    if len(l) < 10:
                        l.append(len(s))
                    elif l[-1] == "fin":
                        pass
                    else:
                        if l[-2] == len(s):
                            l.append("fin")
                        else:
                            l.append(len(s))
                if k not in first_ever:
                    first_ever[k] = step
                
            new_locations = set()
            for loc in locations:
                for adj in ((1,0), (-1,0), (0,1), (0,-1)):
                    yy, xx = loc[0] + adj[0], loc[1] + adj[1]
                    ymod = yy % height
                    xmod = xx % width
                    t = tiles.get((ymod, xmod)) 
                    if t == "S" or t == ".":
                        new_locations.add((yy, xx))
            locations = new_locations
            # Magic Factor: early return & switch into arithmetic solution.
            # TODO: how to figure out automatically that we've proceeded far enough?
            if width > 100:
                factor = 3 * max(width, height)
                factor = 4 * max(width, height)
            else:
                factor = 5 * max(width, height)
            if step > factor:
                #print("stepping out early at", step)
                verify = False
                break

        import pickle
        if width > 100:
            with open("locations.pickle", "wb") as f:
                obj = (locations, size_per_loc, first_ever, verify, steps)
                pickle.dump(obj, f)

    # how many unique starts?
    #print("first len", len(first))
    #print("first len, unique st", len(set((st for (pos, st) in first.keys()))))

    paths = set()
    for p in size_per_loc.values():
        p = tuple(p)
        paths.add(p)
    #print("unique paths", len(paths), len(size_per_loc))
    path_order = list(paths)
    del paths
    
    # The diamond visualization
    min_x = min(x for (_, x) in size_per_loc.keys())
    s = ""
    s2 = ""
    next_row = ""
    yy = 0
    diamond = {}
    for (y,x), path in sorted(size_per_loc.items()):
        if y != yy:
            if s:
                s += "\n"
                s2 += next_row + "\n"
            next_row = "   "
            s += f"{y:>3}"
            s += "    " * (x-min_x)
            next_row += "    " * (x-min_x)
            yy = y
        v = path_order.index(tuple(path))
        s += f"{v:>3} "
        f = first_ever[(y,x)] 
        next_row += f"{f:>3} "
        diamond[(y,x)] = (v, f)
    s += "\n"
    s2 += next_row + "\n"
    # DIAMOND PRINT
    #print(s)
    #print(s2)

    # steps=26501365
    total_size_at_steps  = 0
    total_size_at_steps_complete = False
    
    parity = steps % 2
    size_of_middle = size_per_loc[(0,0)]
    if size_of_middle[-1] == "fin":
        if len(size_of_middle) % 2 == parity:
            total_size_at_steps += size_of_middle[-2]
        else:
            total_size_at_steps += size_of_middle[-3]

        if verify:
            # Verification
            middle_verified = 0
            for l in locations:
                i, y = divmod(l[0], height)
                j, x = divmod(l[1], width)
                if i == 0 and j == 0:
                    middle_verified += 1
            assert total_size_at_steps == middle_verified
            # Verification
        
    for cardinal in ((1,0), (-1, 0), (0, -1), (0, 1)):
        p = 0, 0
        p = p[0] + cardinal[0], p[1] + cardinal[1]
        prev_diff = 0
        d = 1
        diff = None
        path = None
        min_d = None
        while True:
            
            np = p[0] + cardinal[0], p[1] + cardinal[1]
            if np not in diamond:
                break
            dnp = diamond[np] 
            dp = diamond[p]
            #print("cardinal", cardinal, p, diff, prev_diff, dnp[0], dp[0])
            diff = dnp[1] - dp[1]
            
            if diff == prev_diff:
                path = path_order[dp[0]]
                next_path = path_order[dnp[0]]
                assert path[0:len(next_path)] == next_path
                if path[-1] != "fin":
                    break
                min_d = d
                break
            prev_diff = diff
            p = np
            d += 1
        if path is None or min_d is None:
            #print("quick return in cardinal")
            continue
        loc = cardinal[0] * min_d, cardinal[1] * min_d
        steps_at_d = diamond[loc][1]
        #print(cardinal, "got", diff, path, min_d, steps_at_d)

        size_of_cardinal = 0
        for d in range(1, min_d):
            loc = cardinal[0] * d, cardinal[1] * d
            size_of_tile = size_per_loc[loc]
            assert size_of_tile[-1] == "fin"
            #assert tuple(size_per_loc[loc]) == path
            steps_at_local_d = diamond[loc][1]
            parity = (steps - steps_at_local_d) % 2
            
            if len(size_of_tile) % 2 == parity: # TODO ?
                size_of_cardinal += size_of_tile[-2]
                #print("add ", size_of_tile[-2], "for", loc, "foo")
            else:
                size_of_cardinal += size_of_tile[-3]
                #print("add ", size_of_tile[-3], "for", loc, "bar")

        # how about the others:
        d, m = divmod(steps - steps_at_d, diff)
        #print(steps, "DIvMOD ", diff, " IS ", d, m)
        assert m + diff * 2 >= len(path)
        parity = (steps - steps_at_d) % 2

        d_minus_two = d - 1
        evens = d_minus_two//2
        odds = d_minus_two//2
        if d_minus_two % 2 == 1:
            if parity == 1:
                odds += 1
            else:
                evens += 1
        assert odds + evens == d_minus_two
        # assert tuple(size_per_loc[loc]) == path

        # If this fails, next assumptions don't hold.
        assert diff % 2 == 1
        
        #print("have here", evens, odds, min_d, d, m, parity, len(path) % 2)
        
        # steps left: steps - steps_at_d
        # parity == steps left % 2
        
        if len(path) % 2 == 1:
            #print("ok ",  path[-2], "times", odds)
            size_of_cardinal += path[-2] * odds
            #print("ok ",  path[-3], "times", evens)
            size_of_cardinal += path[-3] * evens
        else:
            #print("ok ",  path[-2], "times", evens)
            size_of_cardinal += path[-2] * evens
            #print("ok ",  path[-3], "times", odds)
            size_of_cardinal += path[-3] * odds


        size_of_cardinal += path[m]
        prev_row = m + diff
        while prev_row >= len(path) or path[prev_row] == "fin":
            prev_row -= 2
        size_of_cardinal += path[prev_row]
        #print("two more ",  path[prev_row], "and", path[m])
        
        total_size_at_steps += size_of_cardinal
        
        if verify:
            # Verification
            cardinal_verified = 0
            for l in locations:
                i, y = divmod(l[0], height)
                j, x = divmod(l[1], width)

                ii = math.copysign(1, i) if i != 0 else 0
                jj = math.copysign(1, j) if j != 0 else 0

                if cardinal == (ii, jj):
                    cardinal_verified += 1
            #print(size_of_cardinal, cardinal_verified)
            assert size_of_cardinal == cardinal_verified
            # Verification

    # non-cardinals
    def gen_pos(direction, distance):
        coordinate = direction[0] * 0, direction[1] * distance
        while True:
            next_coord = coordinate[0] + direction[0], coordinate[1]  - direction[1]
            if next_coord[1] != 0:
                yield next_coord
            else:
                break
            coordinate = next_coord
        
    for direction in ((1, 1), (1, -1), (-1, -1), (-1, 1)):
        d = 0
        prev_steps_at = None
        prev_diff = None
        paths_by_distance = []
        while True:
            d += 1
            paths = []
            steps_at = []
            for p in gen_pos(direction, d):
                assert p in diamond
                f, r = diamond[p]
                paths.append(f)
                steps_at.append(r)
                prev_diff = diff
            
            if len(set(paths)) == 1 and len(set(steps_at)) == 1:
                paths = paths[0]
                paths_by_distance.append(paths)
                steps_at = steps_at[0]
                if prev_steps_at is not None:
                    diff = steps_at - prev_steps_at
                    if prev_diff is not None:
                        if diff == prev_diff:
                            steps_at_d = steps_at
                            min_d = d
                            path = path_order[paths]
                            while path[-1] != "fin":
                                paths = paths_by_distance.pop()
                                path = path_order[paths]
                            assert path[-1] == "fin"
                            #print("direction", steps_at_d, min_d, path)
                            break
                    prev_diff = diff
                prev_steps_at = steps_at
                
                size_of_cardinal = 0

        size_of_direction = 0

        for d in range(1, min_d):
            for loc in gen_pos(direction, d):
                size_of_tile = size_per_loc[loc]
                assert size_of_tile[-1] == "fin"
                steps_at_local_d = diamond[loc][1]
                parity = (steps - steps_at_local_d) % 2
                
                if len(size_of_tile) % 2 == parity: # TODO ?
                    size_of_direction += size_of_tile[-2]
                    #print("add ", size_of_tile[-2], "for", loc, "fooz", parity)
                else:
                    size_of_direction += size_of_tile[-3]
                    #print("add ", size_of_tile[-3], "for", loc, "barz", parity)

        d, m = divmod(steps - steps_at_d, diff)
        #print(steps, "DIVMOD ", diff, " IS ", d, m)
        assert m + diff * 2 >= len(path)
        parity = (steps - steps_at_d) % 2

        # If this fails, next assumptions don't hold.
        assert diff % 2 == 1

        d_minus_two = d + min_d - 2
        def asum(a1, an):
            a1 -= 1
            an -= 1
            n = (an - a1)/2 + 1
            return int(n * (a1 + an) // 2)
        d_minus_two_row_nr = d_minus_two
        # Need 2 and 6, 3 and 5.
        if (d_minus_two_row_nr - min_d) % 2 == 0:
            t1 = asum(min_d, d_minus_two_row_nr)
            t2 = asum(min_d + 1, d_minus_two_row_nr - 1)
        else:
            t1 = asum(min_d, d_minus_two_row_nr - 1)
            t2 = asum(min_d + 1, d_minus_two_row_nr)
        
        #print("teets", t1, t2)
        #print(d_minus_two, min_d, d_minus_two_row_nr, steps_at_d, "hmm", path[-2], path[-3], t1, t2)
        if t1 < 0 or t2 < 0:
            #print("quick return in direction")
            continue

        if len(path) % 2 == parity:
            #print("ok ",  path[-2], "times", t1)
            size_of_direction += path[-2] * t1
            #print("ok ",  path[-3], "times", t2)
            size_of_direction += path[-3] * t2
        else:
            #print("ok ",  path[-2], "times", t2)
            size_of_direction += path[-2] * t2
            #print("ok ",  path[-3], "times", t1)
            size_of_direction += path[-3] * t1

        last_row = d + min_d - 1
        #print("two more ",  path[m + diff], "times", (last_row - 1), "and", path[m], "times", last_row)
        size_of_direction += path[m] * last_row
        prev_row = m + diff
        while prev_row >= len(path) or path[prev_row] == "fin":
            prev_row -= 2
        size_of_direction += path[prev_row] * (last_row - 1)

        total_size_at_steps += size_of_direction

        if verify:
            # Verification
            direction_verified = 0
            for l in locations:
                i, y = divmod(l[0], height)
                j, x = divmod(l[1], width)

                ii = math.copysign(1, i) if i != 0 else 0
                jj = math.copysign(1, j) if j != 0 else 0

                if direction == (ii, jj):
                    direction_verified += 1
            #print(size_of_direction, direction_verified)
            assert size_of_direction == direction_verified
            # Verification
        total_size_at_steps_complete = True

    if verify:
        if not total_size_at_steps_complete:
            #print("arithmetic solution returned early?")
            #print(len(locations), total_size_at_steps)
            pass
        else:
            #print("verified against brute force")
            #print(len(locations), total_size_at_steps)
            assert len(locations) == total_size_at_steps
    if total_size_at_steps_complete:
        #for loc, path in size_per_loc.items():
        #    if abs(loc[0]) in (-1, 0, 1) and abs(loc[1]) in (-1, 0, 1):
        #        print(loc, path[-3:])
        return total_size_at_steps
    else:
        return len(locations)

assert(part2(test, 100) == 6536)
assert(part2(test, 110) == 7934)
assert(part2(test, 111) == 8078)
assert(part2(test, 112) == 8242)
assert(part2(test, 500) == 167004)
assert(part2(test, 1000) == 668697)
assert(part2(test, 5000) == 16733044)


assert(part2(data, 400) == 137777)
assert(part2(data, 421) == 152521)
assert(part2(data, 446) == 170781)
assert(part2(data, 500) == 215404)    
assert(part2(data, 458) == 180683)
print(ans := part2(data))
