import os.path

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def part1(data, prize_shift = 0):
    machines = data.split("\n\n")
    mach = []
    for machine in machines:
        a, b, prize = machine.splitlines()
        p = a.split("+")
        ax = int(p[1].split(",")[0])
        ay = int(p[2])
        p = b.split("+")
        bx = int(p[1].split(",")[0])
        by = int(p[2])
        p = prize.split("=")
        px = int(p[1].split(",")[0]) + prize_shift
        py = int(p[2]) + prize_shift
        mach.append(((ax,ay),(bx,by),(px,py)))
    
    s = 0
    for ((ax,ay),(bx,by),(px,py)) in mach:
        # n * ax + m * bx = px
        # n * ay + m * by = py
        # n = (px - m * bx) / ax
        # n = (py - m * by) / ay
        # ax * (py - m * by)  = ay * (px - m * bx)
        # ax * py - m * ax * by = ay * px - m * ay * bx
        # ax * py - ay * px = m * ax * by - m * ay * bx
        # ax * py  - ay * px = m * (ax * by - ay * bx)
        # m = (ax * py - ay * px)/(ax * by - ay * bx)
        m = (ax * py - ay * px)/(ax * by - ay * bx)
        n = (px - m * bx)/(ax)
        
        if int(m) == m and int(n) == n:
            s += int(m) + 3 * int(n)
    return s

test = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""
print(part1(test))
print(part1(data))

def part2(data):
    return part1(data, prize_shift=10000000000000)

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))