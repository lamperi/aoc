import os.path
import re

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def part1(data):
    matches = re.findall(r'mul\((\d+),(\d+)\)', data)
    s = 0
    for m in matches:
        a,b = m
        a = int(a)
        b = int(b)
        s += a*b
    return s

test = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""
print(part1(test))
print(part1(data))

def part2(data):
    matches = re.findall(r"(mul\((\d+),(\d+)\)|do\(\)|don't\(\))", data)
    s = 0
    enabled = True
    for m in matches:
        match m:
            case (w,a,b) if w.startswith("mul"):
                if enabled:
                    a = int(a)
                    b = int(b)
                    s += a*b
            case ("don't()", _, _):
                enabled = False
            case ("do()", _, _):
                enabled = True
    return s

# Override test for part 2.
test = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""

print(part2(test))
print(part2(data))