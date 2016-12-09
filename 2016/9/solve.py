import collections
import re

with open("input.txt") as file:
    data = file.read()


def decompress(data, debug=False):
    u = []
    marker = False
    repeat = None
    times = None
    rep = 0
    tim = 0 
    buf = []
    for c in data:
        if debug: print("CHAR " + c)
        if rep == 0 and c == "(":
            if debug: print("START REP")
            marker = True
            repeat = []
            times = None
        elif marker and c == "x":
            if debug: print("COMMA")
            rep = int("".join(repeat))
            repeat = None
            times = []
        elif marker and times is None and repeat is not None:
            if debug: print("MORE REP")
            repeat.append(c)
        elif marker and c == ")":
            tim = int("".join(times))
            times = None
            marker = False
            if debug: print("END REP {} x {}".format(rep, tim))
        elif marker and times is not None:
            if debug: print("MORE TIM")
            times.append(c)

        elif rep > 0:
            buf.append(c)
            rep -= 1
            if rep == 0:
                for x in range(tim):
                    for b in buf:
                        u.append(b)
                buf = []
        else:
            u.append(c)
    return "".join(u)
            

# tests
print(decompress("ADVENT"))
print(decompress("A(1x5)BC"))
print(decompress("(3x3)XYZ"))
print(decompress("A(2x2)BCD(2x2)EFG"))
print(decompress("(6x1)(1x3)A"))
print(decompress("X(8x2)(3x3)ABCY"))

print("**** PART 1:")
print(len(decompress(data).strip()))
print("****")

def decompress_len(data, debug=False):
    marker = False
    repeat = None
    times = None
    reps = []
    tims = []
    bufs = [0]
    for c in data:
        if debug: print("CHAR " + c)
        for i in range(len(reps)):
            reps[i] -= 1

        if c == "(":
            if debug: print("START REP")
            marker = True
            repeat = []
            times = None
        elif marker and c == "x":
            if debug: print("COMMA")
            rep = int("".join(repeat))
            repeat = None
            times = []
        elif marker and times is None and repeat is not None:
            if debug: print("MORE REP")
            repeat.append(c)
        elif marker and c == ")":
            tim = int("".join(times))
            times = None
            marker = False
            if debug: print("END REP {} x {}".format(rep, tim))
            reps.append(rep)
            tims.append(tim)
            bufs.append(0)
        elif marker and times is not None:
            if debug: print("MORE TIM")
            times.append(c)
        else:
            if debug: print("Inc buf level {} to {} with {} (buf remaining {})".format(len(bufs), bufs[-1]+1, c, reps[-1] if len(reps) else None))
            bufs[-1] += 1
            while len(reps) and reps[-1] == 0:
                l = bufs[-1]
                t = tims[-1]
                reps.pop()
                tims.pop()
                bufs.pop()
                bufs[-1] += l * t
                if debug: print("Append {}x{}={}".format(l,t,l*t))
    return bufs[-1]

print(decompress_len("(3x3)XYZ"))
print(len("XABCABCABCABCABCABCY"))
print(decompress_len("X(8x2)(3x3)ABCY"))
print(decompress_len("(27x12)(20x12)(13x14)(7x10)(1x12)A"))
print(decompress_len("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN"))

print("**** PART 2:")
print(decompress_len(data))
print("****")

