import os.path
import collections
import re
import math
import itertools
INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

def adj_seats1(lines, y, x):
    adj = []
    for yd in (-1, 0, 1):
        for xd in (-1, 0, 1):       
            if yd == 0 and xd == 0:
                continue
            xx = x + xd
            yy = y + yd
            if 0 <= yy < len(lines) and 0 <= xx < len(lines[yy]):
                if lines[yy][xx] != '.':
                    adj.append((yy, xx))
    return adj

def adj_seats2(lines, y, x):
    adj = []
    for yd in (-1, 0, 1):
        for xd in (-1, 0, 1):       
            if yd == 0 and xd == 0:
                continue
            xx = x
            yy = y
            while True:
                xx = xx + xd
                yy = yy + yd
                if 0 <= yy < len(lines) and 0 <= xx < len(lines[yy]):
                    if lines[yy][xx] != '.':
                        adj.append((yy, xx))
                        break
                else:
                    break
    return adj

def adj_map(lines, seat_finder):
    adj_m = {}
    for y, line in enumerate(lines):
        for x, _ in enumerate(line):
            a = seat_finder(lines, y, x)
            adj_m[(y,x)] = a
    return adj_m

def get_adj(lines, adj):
    for y, x in adj:
        yield lines[y][x]

def internal_solve(data, seat_finder, next_to_seats):
    lines = data.split("\n")
    t = 0
    adj_m = adj_map(lines, seat_finder)
    while True:
        t += 1
        new_lines = []
        changes = 0
        for y, line in enumerate(lines):
            new_line = []
            for x, c in enumerate(line):
                adj_seats = list(get_adj(lines, adj_m[(y,x)]))
                if c == "L" and '#' not in adj_seats:
                    new_line.append('#')
                    changes+=1
                elif c == "#" and adj_seats.count('#') >= next_to_seats:
                    new_line.append('L')
                    changes+=1
                else:
                    new_line.append(c)
            new_lines.append(new_line)
        lines = new_lines
        if changes == 0:
            #print("\n".join("".join(line) for line in lines))
            #print(t)
            break

    seats = 0
    for line in lines:
        seats += line.count("#")
    return seats

def solve1(data):
    return internal_solve(data, adj_seats1, 4)

def solve2(data):
    return internal_solve(data, adj_seats2, 5)

print(solve1("""L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""))
print(solve1(data))

print(solve2("""L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""))
print(solve2(data))
