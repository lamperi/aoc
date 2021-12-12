import os.path
INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read().strip()

def func(data):
    s = 0
    for line in data.splitlines():
        w = line.split()
        if len(w) == len(set(w)):
            s += 1
    return s

print(func(data))


def func(data):
    s = 0
    for line in data.splitlines():
        w = [str(sorted(list(ww))) for ww in line.split()]
        if len(w) == len(set(w)):
            s += 1
    return s

print(func(data))
