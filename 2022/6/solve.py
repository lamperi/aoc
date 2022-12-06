import os.path
import re

FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(FILE) as f:
    INPUT = f.read()

TEST = """mjqjpqmgbljsphdztnvjfqwrcgsmlb"""

def ints(line):
    return map(int, re.findall("\d+", line))

def solve(data, n):
    for i in range(len(data)-n):
        if len(set(data[i:i+n])) == n:
            return i+n

print(solve(TEST, 4))
print(solve(INPUT, 4))
print(solve(TEST, 14))
print(solve(INPUT, 14))
