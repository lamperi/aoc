import os.path
from collections import Counter

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def part1(data):
    stones = [int(s) for s in data.strip().split()]
    for _i in range(25):
        new_stones = []
        for s in stones:
            ss = str(s)
            l = len(ss)
            if s == 0:
                new_stones.append(1)
            elif l % 2 == 0:
                n1 = int(ss[:l//2])
                n2 = int(ss[l//2:])
                new_stones.append(n1)
                new_stones.append(n2)
            else:
                new_stones.append(s * 2024)
        stones = new_stones
    return len(stones)

test = """125 17"""
print(part1(test))
print(part1(data))

def part2(data):
    stones = [int(s) for s in data.strip().split()]
    stones = Counter(stones)
    for _i in range(75):
        new_stones = Counter()
        for s,num in stones.items():
            ss = str(s)
            l = len(ss)
            if s == 0:
                new_stones[1] += num
            elif l % 2 == 0:
                n1 = int(ss[:l//2])
                n2 = int(ss[l//2:])
                new_stones[n1] += num
                new_stones[n2] += num
            else:
                new_stones[s * 2024] += num
        stones = new_stones
    return sum(stones.values())

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))