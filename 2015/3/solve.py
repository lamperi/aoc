import re

with open("input.txt") as file:
    data = file.read()

# PART 1

visited = set()

x,y = 0,0
visited.add((x,y))
for c in data:
    if c == "^":
        y += 1
    elif c == ">":
        x += 1
    elif c == "<":
        x -= 1
    else:
        y -= 1
    visited.add((x,y))

print(len(visited))

# PART 2

visited = set()

x1,y1 = 0,0
x2,y2 = 0,0
visited.add((x1,y1))
for e, c in enumerate(data):
    if e % 2:
        if c == "^":
            y1 += 1
        elif c == ">":
            x1 += 1
        elif c == "<":
            x1 -= 1
        else:
            y1 -= 1
        visited.add((x1,y1))
    else:
        if c == "^":
            y2 += 1
        elif c == ">":
            x2 += 1
        elif c == "<":
            x2 -= 1
        else:
            y2 -= 1
        visited.add((x2,y2))

print(len(visited))
