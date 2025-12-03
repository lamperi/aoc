import os.path

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def part1(data):
    joltage = 0
    for battery_bank in data.splitlines():
        battery_bank = [int(c) for c in battery_bank]
        first = max(battery_bank[:-1])
        i = battery_bank.index(first)
        second = max(battery_bank[i+1:])
        total = first*10 + second
        joltage += total
    return joltage

test = """987654321111111
811111111111119
234234234234278
818181911112111"""
print(part1(test))
print(part1(data))

def part2(data):
    total_joltage = 0
    for battery_bank in data.splitlines():
        battery_bank = [int(c) for c in battery_bank]
        index = 0
        joltage = 0
        for cutoff in range(11,-1,-1):
            end_index = len(battery_bank) - cutoff
            digit = max(battery_bank[index:end_index])
            index = battery_bank.index(digit, index) + 1
            joltage = joltage * 10 + digit
        total_joltage += joltage
    return total_joltage

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))