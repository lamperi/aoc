import os.path

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

TEST = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

def part1(data):
    s = 0
    lines = data.splitlines()
    for line in lines:
        n = ""
        for c in line:
            if c.isdigit():
                n += c
        if n:
            n = int(n[0] + n[-1])
            s += n
    return s

print(part1(TEST))
print(part1(data))

TEST = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

def part2(data):
    lines = data.splitlines()
    total = 0
    for line in lines:
        first = len(line)
        last = -1
        first_value = None
        last_value = None
        for s,v in (("one", 1), ("two", 2), ("three", 3), ("four", 4), ("five", 5), ("six", 6), ("seven", 7), ("eight", 8), ("nine", 9)):
            first_index = line.find(s)
            last_index = line.rfind(s)
            if first_index != -1 and first_index < first:
                first = first_index
                first_value = v
            if last_index != -1 and last_index > last:
                last = last_index
                last_value = v
        for s,v in (("1", 1), ("2", 2), ("3", 3), ("4", 4), ("5", 5), ("6", 6), ("7", 7), ("8", 8), ("9", 9), ("0", 0)):
            first_index = line.find(s)
            last_index = line.rfind(s)
            if first_index != -1 and first_index < first:
                first = first_index
                first_value = v
            if last_index != -1 and last_index > last:
                last = last_index
                last_value = v
        assert first_value and last_value, line
        total += 10*first_value + last_value
        
    return total

print(part2(TEST))
print(part2(data))