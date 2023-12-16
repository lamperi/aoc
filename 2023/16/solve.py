import os.path

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def energize(area, pos, dir):
    states = [(pos, dir)]
    energized = {(pos, dir)}
    while states:
        pos, dir = states[0]
        states = states[1:]
        dirs = None
        if pos not in area:
            continue
        match area[pos]:
            case "\\":
                if dir == (0,1):
                    dir = (1,0)
                elif dir == (1,0):
                    dir = (0,1)
                elif dir == (0,-1):
                    dir = (-1,0)
                else:
                    dir = (0,-1)
            case '/':
                if dir == (0,1):
                    dir = (-1,0)
                elif dir == (1,0):
                    dir = (0,-1)
                elif dir == (0,-1):
                    dir = (1,0)
                else:
                    dir = (0,1)
            case '.':
                pass
            case '|':
                if dir[0] == 0:
                    dirs = [(-1,0), (1,0)]
            case '-':
                if dir[1] == 0:
                    dirs = [(0,-1), (0,1)]
            case a:
                assert False, f"has: {a}"
        if dirs is None:
            dirs = [dir]
        for d in dirs:
            p = pos[0]+d[0], pos[1]+d[1]
            if (p, d) not in energized and p in area:
                energized.add((p, d))
                states.append((p, d))
                
    e = set(p for p, _ in energized)
    
    if False:
        s = ""
        for y, line in enumerate(data.splitlines()):
            for x, c in enumerate(line):
                if (y,x) in e:
                    s += "#"
                else:
                    s += "."
            s += "\n"
        print(s)
    
    return len(e)


def part1(data):
    area = {}
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            area[(y,x)] = c
    pos = (0,0)
    dir = (0,1)
    return energize(area, pos, dir)

test = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""
print(part1(test))
print(part1(data))

def part2(data):
    area = {}
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            area[(y,x)] = c
    max_y = max(y for y, _ in area.keys())
    max_x = max(x for _, x in area.keys())
    v = []
    for x in range(max_x+1):
        pos = (0,x)
        dir = (1,0)
        v.append(energize(area, pos, dir))
        
        pos = (max_y,x)
        dir = (-1,0)
        v.append(energize(area, pos, dir))
    
    for y in range(max_y+1):
        pos = (y,0)
        dir = (0,1)
        v.append(energize(area, pos, dir))
        
        pos = (y,max_x)
        dir = (0, -1)
        v.append(energize(area, pos, dir))
        
    return max(v)

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))