import os.path
from collections import deque, defaultdict

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def evolve(sn):
    h = sn * 64
    sn ^= h
    sn = sn % 16777216
    h = sn // 32
    sn ^= h
    sn = sn % 16777216
    h = sn * 2048
    sn ^= h
    sn = sn % 16777216
    return sn

def part1(data):
    secret_numbers = [int(n) for n in data.splitlines()]
    
    ans = 0
    for sn in secret_numbers:
        for _t in range(2000):
            sn = evolve(sn)
        ans += sn

    return ans

test = """1
10
100
2024"""
assert part1(test) == 37327623
print(part1(data))

def part2(data):
    secret_numbers = [int(n) for n in data.splitlines()]
    
    score_across_numbers = defaultdict(int)
    for sn in secret_numbers:
        window = deque([])
        prices_seen = set()
        last_price = sn
        for _t in range(2000):
            sn = evolve(sn)

            # Price changes
            price = sn % 10
            if last_price is not None:
                change = price - last_price
                if len(window) == 4:
                    window.popleft()
                window.append(change)
                if len(window) == 4:
                    key = tuple(window)
                    if key not in prices_seen:
                        score_across_numbers[key] += price
                        prices_seen.add(key)
            last_price = price

    return max(score_across_numbers.values())

# Override test for part 2.
test = """1
2
3
2024"""

assert part2(test) == 23
print(part2(data))