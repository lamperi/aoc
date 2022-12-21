import os.path
from operator import sub

FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(FILE) as f:
    INPUT = f.read()

TEST = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""

def eval_monkey(monkeys, monkey_id):
    ops = monkeys[monkey_id]
    match ops:
        case a, '=', b:
            return eval_monkey(monkeys, a), eval_monkey(monkeys, b)
        case a, '*', b:
            return eval_monkey(monkeys, a) * eval_monkey(monkeys, b)
        case a, '/', b:
            return eval_monkey(monkeys, a) / eval_monkey(monkeys, b)            
        case a, '+', b:
            return eval_monkey(monkeys, a) + eval_monkey(monkeys, b)
        case a, '-', b:
            return eval_monkey(monkeys, a) - eval_monkey(monkeys, b)
        case one,:
            return int(one)

def solve(data):
    monkeys = {}
    for line in data.splitlines():
        a, b = line.split(": ")
        ops = b.split(" ")
        monkeys[a] = ops

    root = eval_monkey(monkeys, "root")
    return int(root)

def solve2(data):
    monkeys = {}
    for line in data.splitlines():
        a, b = line.split(": ")
        ops = b.split(" ")
        monkeys[a] = ops

    monkeys["root"] = (monkeys["root"][0], "=", monkeys["root"][2])
    # Check to see if the function (a-b) grows for "humn"
    # TEST goes into other direction as INPUT
    monkeys["humn"] = 0,
    c1 = sub(*eval_monkey(monkeys, "root"))
    monkeys["humn"] = 1,
    c2 = sub(*eval_monkey(monkeys, "root"))
    sign = -1 if c1 < c2 else 1

    # Binary search!
    # random number picked from a stdout of earlier iteration and
    # increased a bit.
    lo = -51263532836914
    hi =  51263532836914
    while lo < hi:
        n = (lo + hi)//2
        monkeys["humn"] = (n,)
        a, b = eval_monkey(monkeys, "root")
        if a == b:
            return n
        if sign * (a - b) > 0:
            lo = n
        else:
            hi = n
    return 

print(solve(TEST))
print(solve(INPUT))

print(solve2(TEST))
print(solve2(INPUT))
