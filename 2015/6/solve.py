import re
import numpy as np

with open("input.txt") as file:
    data = file.read()

# PART 1
light = np.zeros((1000,1000))

pattern = r"([\w ]+) (\d+),(\d+) through (\d+),(\d+)"
for command, x1,y1, x2,y2 in re.findall(pattern, data):
    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)
    ix = np.ix_(np.arange(x1,x2+1),np.arange(y1,y2+1))
    if command == "turn on":
        light[ix] = 1
    elif command == "turn off":
        light[ix] = 0
    elif command == "toggle":
        light[ix] = np.logical_xor(1, light[ix])
        
print(sum(sum(light)))

# PART 1
light = np.zeros((1000,1000))

pattern = r"([\w ]+) (\d+),(\d+) through (\d+),(\d+)"
for command, x1,y1, x2,y2 in re.findall(pattern, data):
    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)
    ix = np.ix_(np.arange(x1,x2+1),np.arange(y1,y2+1))
    if command == "turn on":
        light[ix] += 1
    elif command == "turn off":
        light[ix] = np.maximum(light[ix] - 1, 0)
    elif command == "toggle":
        light[ix] += 2
        
print(sum(sum(light)))
