with open("input.txt") as f:
    data = f.read().strip()

import re
import math

moons = []
vels = []
for line in data.splitlines():
    x, y, z = map(int, re.findall('-?\\d+', line))
    moons.append((x,y,z))
    vels.append((0,0,0))

def sim(moons, steps):
    t = 0
    vels = []
    for moon in moons:
        vels.append((0,0,0))
    while True:
        for i, m1, in enumerate(moons):
            for j, m2 in enumerate(moons[i+1:], i+1):
                v1 = vels[i]
                v2 = vels[j]
                nv1 = []
                nv2 = []
                for comp in (0,1,2):
                    if m1[comp] < m2[comp]:
                        nv1.append(v1[comp] + 1)
                        nv2.append(v2[comp] - 1)
                    elif m1[comp] > m2[comp]:
                        nv1.append(v1[comp] - 1)
                        nv2.append(v2[comp] + 1)
                    else:
                        nv1.append(v1[comp])
                        nv2.append(v2[comp])
                 
                vels[i] = tuple(nv1)
                vels[j] = tuple(nv2)
        for i, (moon, vel) in enumerate(zip(moons, vels)):
            moons[i] = (moon[0] + vel[0], moon[1] + vel[1], moon[2] + vel[2])
        t += 1

        #print(moons)
        if t == steps:
            pot = [sum(abs(c) for c in m) for m in moons]
            kin = [sum(abs(c) for c in v) for v in vels]
            part1 =  sum(p*k for p, k in zip(pot, kin))
            return part1
   
        
print(sim([
 (-1, 0, 2),
 (2, -10, -7),
 (4, -8, 8),
 (3, 5, -1)
], 10))

print(sim([
 (-8, -10, 0),
 (5, 5, 10),
 (2, -7, 3),
 (9, -8, -3)
], 100))

print(sim(moons[:], 1000))

def sim_repeat(moons):
    t = 0
    hist = [{}, {}, {}]
    cycle = [[], [], []]
    vels = []
    for moon in moons:
        vels.append((0,0,0))
    while True:
        for i, m1, in enumerate(moons):
            for j, m2 in enumerate(moons[i+1:], i+1):
                v1 = vels[i]
                v2 = vels[j]
                nv1 = []
                nv2 = []
                for comp in (0,1,2):
                    if m1[comp] < m2[comp]:
                        nv1.append(v1[comp] + 1)
                        nv2.append(v2[comp] - 1)
                    elif m1[comp] > m2[comp]:
                        nv1.append(v1[comp] - 1)
                        nv2.append(v2[comp] + 1)
                    else:
                        nv1.append(v1[comp])
                        nv2.append(v2[comp])
                 
                vels[i] = tuple(nv1)
                vels[j] = tuple(nv2)
        for i, (moon, vel) in enumerate(zip(moons, vels)):
            moons[i] = (moon[0] + vel[0], moon[1] + vel[1], moon[2] + vel[2])

        x = tuple(m[0] for m in moons) + tuple(m[0] for m in vels)
        y = tuple(m[1] for m in moons) + tuple(m[1] for m in vels)
        z = tuple(m[2] for m in moons) + tuple(m[2] for m in vels)
        for i, (d, h) in enumerate(zip((x,y,z), hist)):
            if d in h:
                c = t-h[d]
                cycle[i].append((t,c))
            h[d] = t 

        t += 1
        if (all(len(c) for c in cycle)):
            break

    val = []
    for c in cycle:
        assert all(c[0][1] == a[1] for a in c)
        val.append(c[-1][1])
    return lcm(val[0], lcm(val[1], val[2]))

def lcm(a,b):
    return int(a*b/math.gcd(int(a),int(b)))

print(sim_repeat([
 (-1, 0, 2),
 (2, -10, -7),
 (4, -8, 8),
 (3, 5, -1)
]))

print(sim_repeat([
 (-8, -10, 0),
 (5, 5, 10),
 (2, -7, 3),
 (9, -8, -3)
]))
print(sim_repeat(moons[:]))
