import os.path

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def parse_input(data, use_color_as_instructions):
    inst = []
    for line in data.splitlines():
        d, n, color = line.split()
        if use_color_as_instructions:
            match color[-2]:
                case '0':
                    d = 'R'
                case '1':
                    d = 'D'
                case '2':
                    d = 'L'
                case '3':
                    d = 'U'
            n = int(color[2:-2], 16)
        else:
            n = int(n)
        inst.append((d, n))
    return inst

def part1(data):
    inst = parse_input(data, False)
        
    y, x = pos = (0, 0)
    walls = set([pos])
    for (d, n) in inst:
        match d:
            case 'R':
                dx = 1
                dy = 0
            case 'D':
                dx = 0
                dy = 1
            case 'L':
                dx = -1
                dy = 0
            case 'U':
                dx = 0
                dy = -1
        for _ in range(n):
            y, x = pos = y + dy, x + dx
            walls.add(pos)
    # flood fill
    # print(len(walls))
    queue = [(1, 1)]
    fill = set()
    while queue:
        y, x = queue[0]
        queue = queue[1:]
        for dy,dx in ((1,0), (-1,0), (0,1), (0,-1)):
            yy = y+dy
            xx = x+dx
            pos = yy, xx
            if pos not in walls and pos not in fill:
                fill.add(pos)
                queue.append(pos)
    
    return len(walls | fill)

test = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""
print(part1(test))
print(part1(data))

def part2(data):
    inst = parse_input(data, True)

    y, x = pos = (0, 0)
    corners = [pos]
    for (d, n) in inst:
        match d:
            case 'R':
                dx = 1
                dy = 0
            case 'D':
                dx = 0
                dy = 1
            case 'L':
                dx = -1
                dy = 0
            case 'U':
                dx = 0
                dy = -1
        y, x = pos = y + dy * n, x + dx * n

        corners.append(pos)
    assert corners[0] == corners[-1]
    del corners[-1]
    
    assert False


# Override test for part 2.
# test = """ """

print(part2(test))
#print(part2(data))