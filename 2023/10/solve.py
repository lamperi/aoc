import os.path

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def viz(area, path):
    visited_range = (
        max(-1, min(p[0] for p in path)-5), max(p[0] for p in path)+5,
        max(-1, min(p[1] for p in path)-5), max(p[1] for p in path)+5)
    draw = f"    {visited_range[2]+1:<3}\n"
    for y in range(visited_range[0], visited_range[1]):
        draw += f"{y+1:>3} "
        for x in range(visited_range[2], visited_range[3]):
            if (y,x) in path:
                draw += "#"
            else:
                draw += area.get((y,x), ".")
        draw += "  "
        for x in range(visited_range[2], visited_range[3]):
            if (y,x) in path:
                draw += area.get((y,x), ".")
            else:
                draw += "`"

        draw += "\n"
    print(draw)

conn = { # COMING FROM ...
    (-1, 0): ('|', '7', 'F'), # SOUTH
    (1, 0): ('|', 'L', 'J'),  # NORTH
    (0, -1): ('-', 'L', 'F'), # EAST
    (0, 1): ('-', 'J', '7'),  # WEST
}
def neg(t):
    return -t[0], -t[1]

def get_loop(data):
    area = data.splitlines()

    tiles = {}
    start = None
    for y, line in enumerate(area):
        for x, c in enumerate(line):
            tiles[(y,x)] = c
            if c == "S":
                assert start is None
                start = (y,x)
    assert start is not None


    states = []
    real_start = []
    for adj in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        a = start[0] + adj[0], start[1] + adj[1]
        #print(start, a, adj, tiles.get(a, None))
        if tiles.get(a, None) in conn[adj]:
            states.append((a, start))
            real_start.append(adj)
    assert len(states) == 2, states
    real_start = [set(v) for k,v in conn.items() if k not in real_start]
    assert len(real_start) == 2
    real_start = next(iter(real_start[0] & real_start[1]))
    tiles[start] = real_start

    path = {start, states[0][0], states[1][0]}
    
    while states[0][0] != states[1][0] and not (states[0][1] == states[1][0] and states[0][0] == states[1][1]):
        new_states = []
        for state in states:
            node, prev = state
            for adj in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                a = node[0] + adj[0], node[1] + adj[1]
                if a == prev:
                    continue
                #print(state, a, adj, tiles.get(a, None))
                if tiles.get(a, None) in conn[adj] and tiles.get(node) in conn[neg(adj)]:
                    new_states.append((a, node))
                    path.add(a)
        states = new_states
        assert len(states) == 2, states
        
        #viz(tiles, path)
    return tiles, path


def part1(data):
    _, path = get_loop(data)
    return len(path)//2

test = """.....
.S-7.
.|.|.
.L-J.
....."""
print(4, "==", part1(test))
print(part1(data))

def part2(data):
    tiles, path = get_loop(data)
    maybe_start = iter(sorted(path))
    while True:
        start = next(maybe_start)
        q = [start]
        visited = {start}
        within = True
        while q:
            #viz(tiles, visited)

            y,x = q[0]
            q = q[1:]
            # logic here:
            # Our position is shifted by 0.5, 0.5.
            # We can squeeze between tiles as long as they are not connected to each other.
            ds = (
                # pos_shift, top_or_left_shift, bottom_or_right_shift, top_or_left_conn_key
                ((-1, 0), (0, 0), (0, 1), (0, -1)),
                (( 1, 0), (1, 0), (1, 1), (0, -1)),
                (( 0,-1), (0, 0), (1, 0), (-1, 0)),
                (( 0, 1), (0, 1), (1, 1), (-1, 0)),
            )
            for pos_shift, top_or_left_shift, bottom_or_right_shift, top_or_left_conn_key in ds:
                n = y + pos_shift[0], x + pos_shift[1]
                if n in visited:
                    continue
                adj1 = y + top_or_left_shift[0], x + top_or_left_shift[1]
                adj2 = y + bottom_or_right_shift[0], x + bottom_or_right_shift[1]
                if (tiles.get(adj1, None) in conn[top_or_left_conn_key] 
                        and tiles.get(adj2) in conn[neg(top_or_left_conn_key)]):
                    continue
                # If the starting position was outside of the loop, we note that
                # we have escaped and break the loop.
                if n not in tiles:
                    q = []
                    within = False
                    break
                q.append(n)
                visited.add(n)
        if within:
            break
    return len(visited - path)

# Override test for part 2.
print(4, "==", part2("""...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""))

print(8, "==", part2(""".F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""))

print(10, "==", part2("""FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""))

print(part2(data))