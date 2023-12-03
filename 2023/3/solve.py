import os.path
import math

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def part1(data):
    data = data.splitlines()
    handled = set()
    parts = []
    for y, line in enumerate(data):
        for x, c in enumerate(line): 
            if (y,x) in handled:
                continue
            
            if c in '0123456789':
                n = c
                handled.add((y,x))
                x1 = x
                while x1+1 < len(line):
                    x1 += 1
                    if line[x1] in '0123456789':
                        n += line[x1]
                        handled.add((y,x1))
                    else:
                        break
                symbol = None
                #print(f"search symbol for {y}, {x} and {n}")
                for y2 in (y-1, y, y+1):
                    for x2 in range(x-1, x+len(n)+1):
                        if 0 <= y2 < len(data) and 0 <= x2 < len(data[y2]):
                            s = data[y2][x2]
                            if s not in '0123456789.':
                                symbol = s
                if symbol:
                    #print(f"Got {n} for {symbol}")
                    parts.append([int(n), (y, x), symbol])
    s = 0
    for v, _, _ in parts:
        s += v
    return s

test = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
print(part1(test))
print(part1(data))

def part2(data):
    data = data.splitlines()
    handled = set()
    parts = []
    m = {}
    part_id = 1
    for y, line in enumerate(data):
        for x, c in enumerate(line): 
            if (y,x) in m:
                continue
            if c in '0123456789':
                n = c
                c = []
                c.append((y,x))
                x1 = x
                while x1+1 < len(line):
                    x1 += 1
                    if line[x1] in '0123456789':
                        n += line[x1]
                        c.append((y,x1))
                    else:
                        break
                n = int(n)
                for (yy, xx) in c:
                    m[(yy,xx)] = (n, part_id)
                part_id += 1
    s = 0
    for y, line in enumerate(data):
        for x, c in enumerate(line): 
            if c != "*":
                continue
            touching_parts = set()
            ratio = []
            for y2 in (y-1, y, y+1):
                for x2 in range(x-1, x+2):
                    if 0 <= y2 < len(data) and 0 <= x2 < len(data[y2]):
                        if (y2,x2) in m:
                            n, part_id = m[y2,x2]
                            if part_id not in touching_parts:
                                touching_parts.add(part_id)
                                ratio.append(n)
            if len(ratio) == 2:
                s += ratio[0] * ratio[1]
    return s

print(part2(test))
print(part2(data))