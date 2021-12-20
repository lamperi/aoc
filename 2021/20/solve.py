import operator
import os.path
import re
from collections import Counter, defaultdict
from functools import partial, reduce
from heapq import heappop, heappush
from io import TextIOBase
from copy import deepcopy
from itertools import combinations, pairwise, permutations
from math import isfinite, prod

INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

test="""..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
"""

def get_window(image, y, x, d):
    for yd in (-1, 0, 1):
        for xd in (-1, 0, 1):
            if 0 <= y+yd < len(image) and 0 <= x+xd < len(image[y+yd]):
                yield image[y+yd][x+xd]
            else:
                yield d

def get_lit_pixels(data, t):
    enchancement, image = data.split("\n\n")
    # Make image mutable
    image = [[c for c in line] for line in image.splitlines()]
    d = "."
    for _ in range(t):
        # pad image by one pixel because the window is 3x3
        # fill with the appropriate default pixel for the iteration
        image = [[d]*(len(image[0])+2)] + [[d] + line + [d] for line in image] + [[d]*(len(image[0])+2)]
        newimage = deepcopy(image)
        for y in range(0, len(newimage)):
            for x in range(0, len(newimage[y])):
                binary = ["1" if c == "#" else "0" for c in get_window(image, y, x, d)]
                index = int("".join(binary), 2)
                newimage[y][x] = enchancement[index]
        image = newimage
        # Note: depending on what the 0 value enchancement resolves, we need to 
        # change the default fill value of the infinite image.
        if enchancement[0] == "#":
            d = "." if d == "#" else "#"

    return "".join("".join(l) for l in image).count("#")

def part1(data):
    return get_lit_pixels(data, t=2)

print(part1(test))
print(part1(data))

def part2(data):
    return get_lit_pixels(data, t=50)

print(part2(test))
print(part2(data))

