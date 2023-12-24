import os.path

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def parse(data):
    hailstones = []
    for line in data.splitlines():
        pos, vel = line.split(" @ ")
        pos = [int(x) for x in pos.split(", ")]
        vel = [int(x) for x in vel.split(", ")]
        hailstones.append((pos, vel))
    return hailstones

def find_intersection(x1, y1, vx1, vy1, x2, y2, vx2, vy2):
    a1, b1, c1  = vx1, -vx2, (x2 - x1)
    a2, b2, c2  = vy1, -vy2, (y2 - y1)
    denom = a1*b2 - b1*a2
    if denom != 0:
        t1 = (c1 * b2 - b1 * c2) / denom
        t2 = (a1 * c2 - c1 * a2) / denom
        #x = x1 + vx1 * t1
        #xx = x2 + vx2 * t2
        #y = y1 + vy1 * t1
        #yy = y2 + vy2 * t2
        #assert abs(x - xx) < 0.00001
        #assert abs(y - yy) < 0.00001
        return t1, t2
    else:
        return None, None

def part1(data, test):
    hailstones = parse(data)
    test_area = (7, 27) if test else (200000000000000, 400000000000000)

    tprint = print if test else lambda *args: None

    test_area_collisions = 0
    for i, h1 in enumerate(hailstones):
        for j, h2 in enumerate(hailstones[i+1:], start=i+1):
            ((x1, y1, _), (vx1, vy1, _)) = h1
            ((x2, y2, _), (vx2, vy2, _)) = h2
            # equations
            # x1 + vx1 * t1 = x2 + vx2 * t2
            # y1 + vy1 * t1 = y2 + vy2 * t2

            # vx1 * t1 - vx2 * t2 + (x1 - x2) = 0
            # vy1 * t1 - vy2 * t2 + (y1 - y2) = 0
            t1, t2 = find_intersection(x1, y1, vx1, vy1, x2, y2, vx2, vy2)
            if t1 is not None:
                x = x1 + vx1 * t1
                xx = x2 + vx2 * t2
                y = y1 + vy1 * t1
                yy = y2 + vy2 * t2
                if test:
                    assert abs(x - xx) < 0.00001
                    assert abs(y - yy) < 0.00001

            denom = (-vx1 * vy2 + vy1 * vx2)
            if denom != 0:
                t1 = (-vx2 * (y1 - y2) + vy2 * (x1 - x2)) / denom
                t2 = ((x1 - x2) * vy1 - (y1 - y2) * vx1) / denom
                x = x1 + vx1 * t1
                xx = x2 + vx2 * t2
                y = y1 + vy1 * t1
                yy = y2 + vy2 * t2
                x_collides = test_area[0] <= x <= test_area[1]
                y_collides = test_area[0] <= y <= test_area[1]
                if t1 >= 0 and t2 >= 0 and x_collides and y_collides:
                    tprint("collision for ", h1, h2, t1, t2, (y, x), (yy, xx))
                    test_area_collisions += 1
                elif t1 < 0 and t2 < 0:
                    tprint("collision in past for A and B", h1, h2, t1, t2, (y, x), (yy, xx))
                elif t1 < 0:
                    tprint("collision in past for A", h1, h2, t1, t2, (y, x), (yy, xx))
                elif t2 < 0:
                    tprint("collision in past for B", h1, h2, t1, t2, (y, x), (yy, xx))
                elif not x_collides and y_collides:
                    tprint("collision outside of X and Y", h1, h2, t1, t2, (y, x), (yy, xx))
                elif not x_collides:
                    tprint("collision outside of X", h1, h2, t1, t2, (y, x), (yy, xx))
                elif not y_collides:
                    tprint("collision outside of Y", h1, h2, t1, t2, (y, x), (yy, xx))
                else:
                    assert False
                if test:
                    assert abs(x - xx) < 0.00001
                    assert abs(y - yy) < 0.00001
            else:
                if x1 == x2 and y1 == y2:
                    tprint("parallel collision ", h1, h2)
                    test_area_collisions += 1
                else:
                    tprint("parellel", h1, h2)


    return test_area_collisions
                
            


test = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""
print(ans := part1(test, True))
assert ans == 2
print(ans := part1(data, False))
assert ans == 24627

def init_ranges(xi, vxi):
    return [
        ((None, xi), (vxi, None)),
        ((xi, None), (None, vxi))
    ]

def update_ranges(ranges, xi, vxi):
    a = min(xi, ranges[0][0][1])
    b = max(vxi, ranges[0][1][0])
    c = max(xi, ranges[1][0][0])
    d = min(vxi, ranges[1][1][1])
    ranges = [
        ((None, a), (b, None)),
        ((c, None), (None, d))
    ]
    return ranges

def part2(data, test):
    hailstones = parse(data)

    # for each hailstone i holds 3 equations with 7 unknown:
    #  x0 + vx0 * ti = xi + vxi * ti
    #  y0 + vy0 * ti = yi + vyi * ti
    #  z0 + vz0 * ti = zi + vzi * ti
    # Having a system of three hailstones will add up to
    # 9 equations with 9 unknowns. It's solvable. This code
    # will print the equations, they need to be input into a solver.
    s = ""
    for i in range(3):
        ((xi, yi, zi), (vxi, vyi, vzi)) = hailstones[i]
        eq = "\n".join((
            "x0 + vx0 * ti = xi + vxi * ti",
            "y0 + vy0 * ti = yi + vyi * ti",
            "z0 + vz0 * ti = zi + vzi * ti",
        ))
        eq = eq.replace("vxi", str(vxi)).replace("vyi", str(vyi)).replace("vzi", str(vzi))
        eq = eq.replace("xi", str(xi)).replace("yi", str(yi)).replace("zi", str(zi))
        eq = eq.replace("ti", "tuv"[i])
        s += eq + "\n"
    s = s.replace("vx0", "a").replace("vy0", "b").replace("vz0", "c")
    s = s.replace("x0", "x").replace("y0", "y").replace("z0", "z")
    print(s)

    # stop here.
    # paste the equation into
    # https://quickmath.com/webMathematica3/quickmath/equations/solve/advanced.jsp
    # variables set to xyz abc tuv
    # copy abc into velocity, xyz into position. Discard tuv, but they should be positive.

    rock = ((24, 13, 10), (-3, 1, 2)) if test else ((194723518367339, 181910661443432, 150675954587450), (148, 159, 249))

    # verify the answer.
    for hailstone in hailstones:
        ((x1, y1, z1), (vx1, vy1, vz1)) = hailstone
        ((x2, y2, z2), (vx2, vy2, vz2)) = rock
        t = (x2 - x1)/(vx1 - vx2)
        assert t == int(t)
        px1 = x1 + vx1 * t
        py1 = y1 + vy1 * t
        pz1 = z1 + vz1 * t
        px2 = x2 + vx2 * t
        py2 = y2 + vy2 * t
        pz2 = z2 + vz2 * t
        assert px1 == px2 and py1 == py2 and pz1 == pz2

    return sum(rock[0])

# Override test for part 2.
# test = """ """

print(ans := part2(test, True))
assert ans == 47
print(part2(data, False))