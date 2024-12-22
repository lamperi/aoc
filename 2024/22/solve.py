import os.path
from collections import deque

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
    
    price_per_windows = []
    for sn in secret_numbers:
        window = deque([])
        price_per_window = {}
        price_per_windows.append(price_per_window)
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
                    if key not in price_per_window:
                        price_per_window[key] = price
            last_price = price

    unique_windows = set()
    for ppw in price_per_windows:
        unique_windows.update(ppw.keys())

    max_bananas = None
    for window in unique_windows:
        bananas = 0
        for ppw in price_per_windows:
            bananas += ppw.get(window, 0)
        if max_bananas is None or bananas > max_bananas:
            max_bananas = bananas
            #print("max bananas with seq", max_bananas, seq)

    return max_bananas

# Override test for part 2.
test = """1
2
3
2024"""

assert part2(test) == 23
print(part2(data))