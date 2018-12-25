import re

data = open('input.txt').read()

example = """ 0,0,0,0
 3,0,0,0
 0,3,0,0
 0,0,3,0
 0,0,0,3
 0,0,0,6
 9,0,0,0
12,0,0,0"""

def manhattan(p1, p2):
    return sum(abs(c1-c2) for c1,c2 in zip(p1, p2))

def add_to_existing(p0, constellations):
    for constellation in constellations:
        for p in constellation:
            if manhattan(p0, p) <= 3:
                constellation.append(p0)
                return True
    return False

def combine(constellations):
    for i, c1 in enumerate(constellations):
        for j, c2 in enumerate(constellations[i+1:], i+1):
            for p1 in c1:
                for p2 in c2:
                    if manhattan(p1, p2) <= 3:
                        c1.extend(c2)
                        del constellations[j]
                        return True
    return False

def solve(input_data):
    points = []
    for line in input_data.splitlines():    
        nums = list(map(int, re.findall(r'-?\d+', line)))
        points.append(nums)

    constellations = []
    while points:
        p0 = points[0]
        points = points[1:]
        
        found = add_to_existing(p0, constellations)
        if not found:
            constellations.append([p0])

    while True:
        suc = combine(constellations)
        if not suc:
            break

    return len(constellations)

print(solve(example), 2)
print(solve("""-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0"""), 4)
print(solve("""1,-1,0,1
2,0,-1,0
3,2,-1,0
0,0,3,1
0,0,-1,-1
2,3,-2,0
-2,2,0,0
2,-2,0,-1
1,-1,0,-1
3,2,0,2"""), 3)
print(solve("""1,-1,-1,-2
-2,-2,0,1
0,2,1,3
-2,3,-2,1
0,2,3,-2
-1,-1,1,-2
0,-2,-1,0
-2,2,3,-1
1,2,2,0
-1,-2,0,-2"""), 8)

print(solve(data))
