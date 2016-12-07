with open("input.txt") as file:
    data = file.read()
    
import re
import itertools

spoon = []
pattern = r"(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)"
for teaspoon, capacity, durability, flavor, texture, calories in re.findall(pattern, data):
    capacity = int(capacity)
    durability = int(durability)
    flavor = int(flavor)
    texture = int(texture)
    calories = int(calories)
    spoon.append((capacity, durability, flavor, texture, calories))

def calc(a,b,c,d):
    val = []
    for i in range(4):
        v = a * spoon[0][i] + b * spoon[1][i] + c * spoon[2][i] + d * spoon[3][i]
        val.append(max(0, v))
    return reduce(lambda x,y: x*y, val)

def calc_cal(a,b,c,d):
    return a * spoon[0][4] + b * spoon[1][4] + c * spoon[2][4] + d * spoon[3][4]

# PART 1
max_score = 0
stats = None
for a in xrange(0,101):
    if a < 100:
        for b in xrange(0, 101-a):
            if a + b < 100:
                for c in xrange(0, 101-a-b):
                    if a + b + c < 100:
                        d = 100 - a - b - c
                        score = calc(a,b,c,d)
                        if score > max_score:
                            max_score = score
                            stats = (a,b,c,d)
                    elif a + b + c == 100:
                        score = calc(a,b,c,0)
                        if score > max_score:
                            max_score = score
                            stats = (a,b,c,0)
                    else:
                        break
            elif a + b == 100:
                score = calc(a,b,0,0)
                if score > max_score:
                    max_score = score
                    stats = (a,b,0,0)
            else:
                break
    elif a == 100:
        score = calc(a,0,0,0)
        if score > max_score:
            max_score = max_score
            stats = (a,0,0,0)     

print(max_score)
print(stats)

# PART 2
max_score = 0
stats = None
for a in xrange(0,101):
    if a < 100:
        for b in xrange(0, 101-a):
            if a + b < 100:
                for c in xrange(0, 101-a-b):
                    if a + b + c < 100:
                        d = 100 - a - b - c
                        score = calc(a,b,c,d)
                        cal = calc_cal(a,b,c,d)
                        if score > max_score and cal == 500:
                            max_score = score
                            stats = (a,b,c,d)
                    elif a + b + c == 100:
                        score = calc(a,b,c,0)
                        cal = calc_cal(a,b,c,0)
                        if score > max_score and cal == 500:
                            max_score = score
                            stats = (a,b,c,0)
                    else:
                        break
            elif a + b == 100:
                score = calc(a,b,0,0)
                cal = calc_cal(a,b,0,0)
                if score > max_score and cal == 500:
                    max_score = score
                    stats = (a,b,0,0)
            else:
                break
    elif a == 100:
        score = calc(a,0,0,0)
        cal = calc_cal(a,0,0,0)
        if score > max_score and cal == 500:
            max_score = max_score
            stats = (a,0,0,0)     

print(max_score)
print(stats)