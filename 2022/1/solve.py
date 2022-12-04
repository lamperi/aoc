import os.path

FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(FILE) as f:
    INPUT = f.read()

TEST = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""

def solve(data):
    elves = data.split("\n\n")
    calories = [sum(map(int, elf.splitlines())) for elf in elves]
    calories.sort()
    return calories[-1], sum(calories[-3:])

print(solve(TEST))
print(solve(INPUT))