import os.path

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def eight_directions():
    for dy in (-1,0,1):
        for dx in (-1,0,1):
            if dy == dx == 0:
                continue
            yield (dy, dx)

def bounds(area: list[list[str]], y: int, x: int):
    return  0 <= y < len(area) and 0 <= x < len(area[y])

def find_xmas(lines,y0,x0):
    if lines[y0][x0] != "X":
        return 0
    v = 8
    for dy,dx in eight_directions():
        y = y0
        x = x0
        need = "MAS"
        for c in need:
            y += dy
            x += dx
            if not bounds(lines, y, x) or lines[y][x] != c:
                v -= 1
                break
    return v

def part1(data):
    lines = data.splitlines()
    
    s = 0
    for y,line in enumerate(lines):
        for x,_ in enumerate(line):
            v = find_xmas(lines,y,x)
            s += v
    return s

test = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""
print(part1(test))
print(part1(data))

def find_masx(lines,y0,x0):
    if lines[y0][x0] != "A":
        return 0
    diags = [
        [(-1,-1),(1,1)],
        [(-1,1),(1,-1)],
    ]
    for diag in diags:
        need = set(["M","S"])
        got = set()
        for dy,dx in diag:
            y = y0 + dy
            x = x0 + dx
            if bounds(lines, y, x):
                got.add(lines[y][x])
        if got != need:
            return 0
    return 1

def part2(data):
    lines = data.splitlines()
    s = 0
    for y,line in enumerate(lines):
        for x,_ in enumerate(line):
            s += find_masx(lines,y,x)
    return s

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))