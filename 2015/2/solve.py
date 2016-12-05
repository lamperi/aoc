import re

with open("input.txt") as file:
    data = file.read()

pattern = r"(\d+)x(\d+)x(\d+)"

sum = 0
ribbon = 0
for line in data.splitlines():
    for w,h,l in re.findall(pattern, line):
        w = int(w)
        h = int(h)
        l = int(l)
        sum += 2*w*h + 2*w*l + 2*h*l + min(w*h, w*l, h*l)
        
        ribbon += 2*min(w+h, w+l, h+l) + w*h*l
print(sum)

print(ribbon)