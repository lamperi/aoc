import os.path
from functools import cache
from collections import defaultdict

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def can_make(design, patterns):
    if design == "":
        return True
    for p in patterns:
        if design.startswith(p):
            if can_make(design[len(p):], patterns):
                return True
    return False

def part1(data):
    patterns, designs = data.split("\n\n")
    patterns = tuple(patterns.split(", "))
    designs = designs.splitlines()
    
    s = 0
    for design in designs:
        if can_make(design, patterns):
            s += 1
    return s

test = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""
print(part1(test))
print(part1(data))

# Memoize approach with cache.
@cache
def ways_to_make(design, patterns):
    if design == "":
        return 1
    ways = 0
    for p in patterns:
        if design.startswith(p):
            ways += ways_to_make(design[len(p):], patterns)
    return ways

def ways_to_make_dp(design, pattern):
    dp = defaultdict(int)
    dp[0] += 1

    for i in range(1, len(design) + 1):
        prefix = design[0:i]
        for p in pattern:
            if prefix.endswith(p):
                dp[i] += dp[i - len(p)]
    return dp[len(design)]

def part2(data):
    patterns, designs = data.split("\n\n")
    patterns = tuple(patterns.split(", "))
    designs = designs.splitlines()
    
    s = 0
    for design in designs:
        s += ways_to_make(design, patterns)
        
    s2 = 0
    for design in designs:
        s2 += ways_to_make_dp(design, patterns)

    assert s == s2
    return s

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))