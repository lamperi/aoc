import os.path

FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(FILE) as f:
    INPUT = f.read()

TEST = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""

def unsnafu(s):
    base = 1
    total = 0
    for i, c in enumerate(reversed(s)):
        if c == "2":
            total += base * 2
        elif c == "1":
            total += base * 1
        elif c == "0":
            total += base * 0
        elif c == "-":
            total += base * -1
        elif c == "=":
            total += base * -2
        base *= 5
    return total

def snafu(d, j):
    base = 5**j
    while d <= base//2:
        j -= 1
        base //= 5
    ret = ""
    while j >= 0:
        assert (-MAX[j] <= d <= MAX[j])
        for m,c in ((2,"2"), (1,"1"), (0,"0"), (-1,"-"), (-2,"=")):
            if j == 0 and d - m*base != 0:
                continue
            elif not (-MAX[j-1] <= d - m*base <= MAX[j-1]):
                continue
            ret += c
            d -= m*base
            j -= 1
            base //= 5
            break
    return ret


def solve(data):
    s = 0
    for line in data.splitlines():
        s += unsnafu(line)
    ret = snafu(s, 25)
    assert s == unsnafu(ret)
    return ret

MAX = []
BASE = []
max_for = 0
base = 1
for t in range(25):
    max_for += 2*base
    MAX.append(max_for)
    base *= 5

print(solve(TEST))
print(solve(INPUT))
