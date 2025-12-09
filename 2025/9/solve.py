import os.path
from collections import deque
import matplotlib.pyplot as plt
import numpy as np

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def part1(data):
    red_tiles = set()
    for line in data.splitlines():
        x,y = line.split(",")
        x = int(x)
        y = int(y)
        red_tiles.add((y,x))
    
    area = 0
    for (y1,x1) in red_tiles:
        for (y2,x2) in red_tiles:
            width = abs(x2-x1)+1
            height = abs(y2-y1)+1
            area = max(area, width*height)
    return area

test = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""
print(part1(test))
print(part1(data))

def is_contained_inside_red_and_green(t1, t2, tiles):
    xs = t1[1], t2[1]
    ys = t1[0], t2[0]
    x0 = min(xs)
    x1 = max(xs)
    y0 = min(ys)
    y1 = max(ys)
    for x in range(x0, x1+1):
        if (y0,x) not in tiles:
            return False
        if (y1,x) not in tiles:
            return False
    for y in range(y0, y1+1):
        if (y,x0) not in tiles:
            return False
        if (y,x1) not in tiles:
            return False
    return True

def part2(data):
    red_tiles = []
    for line in data.splitlines():
        x,y = line.split(",")
        x = int(x)
        y = int(y)
        red_tiles.append((y,x))
    
    green_tiles = list()
    for a,b in zip(red_tiles, red_tiles[1:] + red_tiles[:1]):
        if a[0] == b[0]: # y
            y = a[0]
            xs = a[1], b[1]
            for x in range(min(xs), max(xs)+1):
                green_tiles.append((y,x))
        else:
            x = a[1]
            ys = a[0], b[0]
            for y in range(min(ys), max(ys)+1):
                green_tiles.append((y,x))
    green_tiles = set(green_tiles)            
    print("Generated borders")
    
    start = red_tiles[0][0]+1, red_tiles[0][1]+1
    queue = deque([start])
    while queue:
        (y,x) = queue.popleft()
        assert y > 0 and x > 0
        for n in ((y+1, x), (y-1, x), (y,x+1), (y,x-1)):
            if n not in green_tiles:
                queue.append(n)
                green_tiles.add(n)
    print("Generated inside")

    area = 0
    
    for i, (y1,x1) in enumerate(red_tiles):
        print(f"Checking tile {i+1}/{len(red_tiles)}")
        for (y2,x2) in red_tiles:
            if is_contained_inside_red_and_green((y1,x1), (y2,x2), green_tiles):
                width = abs(x2-x1)+1
                height = abs(y2-y1)+1
                area = max(area, width*height)
    return area

def check(t1, t2, sides, debug=False):
    xs = t1[1], t2[1]
    ys = t1[0], t2[0]
    x0 = min(xs)
    x1 = max(xs)
    y0 = min(ys)
    y1 = max(ys)
    for (sx0, sx1, sy0, sy1) in sides:
        # y0=1, x0=2, x1=11. The side sy1=1, sy2=3, sx=7 must collide.
        if sx0 == sx1:
            # this side goes y direction
            #          I sx0,sy0
            # x0,y0 #XXIXX# x1,y0 
            #          I sx0,sy1
            if sy0 <= y0 <= sy1 and x0 < sx0 < x1:
                if debug:
                    print("#1", (sx0, sx1, sy0, sy1), (x0, x1, y0))
                return False
            # #2 (5487, 5487, 67580, 68845) (5359, 94880, 48563, 67580)
            if sy0 <= y1 <= sy1 and x0 < sx0 < x1:
                if debug:
                    print("#2", (sx0, sx1, sy0, sy1), (x0, x1, y0, y1))
                return False
        else:
            if sx0 <= x0 <= sx1 and y0 < sy0 < y1:
                if debug:
                    print("#3", (sx0, sx1, sy0, sy1), (x0, y0, y1))
                return False
            if sx0 <= x1 <= sx1 and y0 < sy0 < y1:
                if debug:
                    print("#4", (sx0, sx1, sy0, sy1), (x1, y0, y1))
                return False
    return True

def part2fast(data):
    red_tiles = []
    for line in data.splitlines():
        x,y = line.split(",")
        x = int(x)
        y = int(y)
        red_tiles.append((y,x))
    
    sides = [p for p in zip(red_tiles, red_tiles[1:] + red_tiles[:1])]
    better_sides = []
    for s1, s2 in sides:
        xs = s1[1], s2[1]
        ys = s1[0], s2[0]
        sx0 = min(xs)
        sx1 = max(xs)
        sy0 = min(ys)
        sy1 = max(ys)
        better_sides.append((sx0, sx1, sy0, sy1))
    
    if False:
        x = []
        y = []
        for (y0,x0),(y1,x1) in sides:
            x.append(x0)
            x.append(x1)
            y.append(y0)
            y.append(y1)
        fig, ax = plt.subplots()
        ax.plot(x, y)
        plt.show()
    
    correct_tiles = []
    if len(red_tiles) > 10:
        important = []
        for (y,x) in red_tiles:
            if 48563 <= y <= 50218 and 94880 <= x <= 94880:
                important.append((y,x))
        important.sort()
        important1 = important[0]
        important2 = important[1]
        
        crossing = []
        for t1,t2 in sides:
            if min(t1[1], t2[1]) < important1[1] < max(t1[1], t2[1]):
                crossing.append((t1[0], max(t1[1], t2[1])))
        crossing.sort()
        
        # good find: (68131, 95140) (68131, 94757)
        # good find: (33602, 94518) (33602, 94946)
        
        p = crossing[0]
        max_area = 0
        for (y,x) in red_tiles:
            if p[0] <= y <= important1[0] and x < p[1]:
                width = abs(important1[1]-x)+1
                height = abs(important1[0]-y)+1
                area = width*height
                max_area = max(max_area, area)
                if area == max_area:
                    correct_tiles = (y,x), important1
        print("area", max_area)

        p = crossing[1]
        for (y,x) in red_tiles:
            if important2[0] <= y <= p[0] and x < p[1]:
                width = abs(important2[1]-x)+1
                height = abs(important2[0]-y)+1
                area = width*height
                max_area = max(max_area, area)
                if area == max_area:
                    correct_tiles = (y,x), important1
        print("area", max_area, "tiles", correct_tiles)
    
    area = 0
    tiles = None
    for i, (y1,x1) in enumerate(red_tiles):
        for (y2,x2) in red_tiles[i+1:]:
            if (y1,x1) in correct_tiles and (y2,x2) in correct_tiles:
                c = check((y1,x1), (y2,x2), better_sides, True)
                print("foobar", c)
            if check((y1,x1), (y2,x2), better_sides):
                width = abs(x2-x1)+1
                height = abs(y2-y1)+1
                area = max(area, width*height)
                if area > 1554370486:
                    print("Not ok", (y1,x1), (y2,x2))
                tiles = (y1,x1), (y2,x2)
    print(tiles)
    return area


# Override test for part 2.
# test = """ """

print(part2(test))
print(part2fast(test))
print(part2fast(data))
print("Not ok: 1552148022")
print("Not ok: 1464613360")
print("Not ok: 1460393040")
print("ok: 1554370486")