import os.path

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def find_target(target, operands, part2):
    assert len(operands) > 0
    current = operands[0]
    max_i = len(operands)

    def _recurse(c, i):
        if i == max_i:
            return c == target
        # All operations are increasing, so we can shortcut if we
        # are over the target.
        if c > target:
            return False
        n = operands[i]
        if _recurse(c + n, i + 1):
            return True
        if _recurse(c * n, i + 1):
            return True
        if part2:
            if _recurse(int(str(c) + str(n)), i + 1):
                return True
        return False

    return _recurse(current, 1)

def parse(data):
    eq = []
    for line in data.splitlines():
        target, operands = line.split(": ")
        target = int(target)
        operands = [int(v) for v in operands.split()]
        eq.append((target, operands))
    return eq

def part1(data):
    eq = parse(data)
    return sum(target for target, operands in eq if find_target(target, operands, False))

test = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""
print(part1(test))
print(part1(data))

def part2(data):
    eq = parse(data)
    return sum(target for target, operands in eq if find_target(target, operands, True))

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))