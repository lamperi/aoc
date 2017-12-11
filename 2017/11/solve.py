import sys, operator, functools, binascii
data = open("input.txt").read().strip()

def hex_dist(coords):
    
    if abs(coords[0]) > abs(coords[1]):
         return abs(coords[1]) + int((abs(coords[0]) - abs(coords[1]))/2)
    else:
        return abs(coords[1])
    
# PART 1 & PART 2

def func(data):
    inst = data.split(",")
    coords = 0, 0
    max_dist = 0
    for i in inst:
        if i == "ne":
            coords = coords[0] + 1, coords[1] + 1
        elif i == "se":
            coords = coords[0] - 1, coords[1] + 1
        elif i == "s":
            coords = coords[0] - 2, coords[1]
        elif i == "sw":
            coords = coords[0] - 1, coords[1] - 1
        elif i == "nw":
            coords = coords[0] + 1, coords[1] - 1
        elif i == "n":
            coords = coords[0] + 2, coords[1]
        max_dist = max(hex_dist(coords), max_dist)
    return coords, hex_dist(coords), max_dist
        
print(func("ne,ne,ne"), 3)
print(func("ne,ne,sw,sw"), 0)
print(func("ne,ne,s,s"), 2)
print(func("se,sw,se,sw,sw"), 3)
print(func(data))

