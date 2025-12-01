import os.path

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def part1(data):
    dial = 50
    sol = 0
    for inst in data.splitlines():
        d, n = inst[0], inst[1:]
        n = int(n)
        if d == "R":
            dial = (dial + n) % 100
        else:
            dial = (dial - n) % 100
        if dial == 0:
            sol += 1
    return sol

test = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""
print(part1(test))
print(part1(data))

def part2(data):
    dial = 50
    sol = 0
    for inst in data.splitlines():
        d, n = inst[0], inst[1:]
        n = int(n)
        if d == "R":
            dial += n
            sol += dial // 100
            dial %= 100
        else:
            was_zero = dial == 0
            dial -= n
            if dial <= 0:
                if not was_zero:
                    sol += 1
                sol += -dial // 100
            dial %= 100
    return sol

print(part2(test))
print(part2(data))