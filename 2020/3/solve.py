import os.path
import collections
import re
import math
INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

test_data = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""

def solve(data, dy=1, dx=3):
    data=data.splitlines()
    y,x=0,0
    s=0
    while True:
        x = (x+dx) % len(data[y])
        y+=dy
        if y >= len(data) or x >= len(data[y]):
            break
        if data[y][x] == "#":
            s+=1
    return s

def solve2(data):
    p=1
    for dy, dx in (1,1), (1,3), (1,5), (1,7), (2,1):
        p *= solve(data, dy=dy, dx=dx)
    return p

print(solve(test_data), 7)
print(solve2(test_data), 336)

print(solve(data))
print(solve2(data))

