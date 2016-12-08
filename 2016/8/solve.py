import collections
import re

with open("input.txt") as file:
    data = file.read()

W=50
H=6

#W=7
#H=3

display = ['.'*W for i in range(H)]

adata = """rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1"""

# PART 1
for command in data.splitlines():
    print("\n".join(display) + "\n")
    print(command)
    p = command.split()
    if p[0] == "rect":
        w,h = p[1].split("x")
        w = int(w)
        h = int(h)
        for i in range(h):
            display[i] = '*'*w + display[i][w:]
    elif p[0] == "rotate":
        if p[1] == "row":
            y = int(p[2].split("=")[1])
            n = int(p[4])
            m = n % W
            display[y] = display[y][-m:] + display[y][:-m]
        elif p[1] == "column":
            x = int(p[2].split("=")[1])
            n = int(p[4])
            m = n % H
            tp = ["".join(r) for r in zip(*display)]
            #print("tp0\n" + "\n".join(tp) + "\n")
            tp[x] = tp[x][-m:] + tp[x][:-m]
            #print("tp1\n" + "\n".join(tp) + "\n")
            display = ["".join(r) for r in zip(*tp)]

print("\n".join(display))
print(sum(1 for r in display for c in r if c == '*'))

# PART 2
# UPOJFLBCEZ