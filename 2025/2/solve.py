import os.path

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def is_invalid(n):
    s = str(n)
    j = len(s)//2
    return s[:j] == s[j:]

assert not is_invalid(101)
assert is_invalid(11)
assert is_invalid(22)
assert is_invalid(6464)
assert is_invalid(123123)
assert is_invalid(1188511885)

def part1(data):
    ans = 0
    for id_range in data.split(","):
        low,hi = id_range.split("-")
        low = int(low)
        hi = int(hi)
        for n in range(low, hi+1):
            if is_invalid(n):
                ans += n
    return ans

test = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124"""
print(part1(test))
print(part1(data))

def is_invalid_p2(n):
    s = str(n)
    ls = len(s)
    for k in range(1, len(s)//2+1):
        if ls % k != 0:
            continue
        p = [s[j:j+k] for j in range(0, len(s), k)]
        if all(pp == p[0] for pp in p[1:]):
            return True
    return False

assert is_invalid_p2(111)
assert is_invalid_p2(99)
assert is_invalid_p2(38593859)
assert is_invalid_p2(824824824)
assert is_invalid_p2(2121212121)
assert is_invalid_p2(565656)

def part2(data):
    ans = 0
    for id_range in data.split(","):
        low,hi = id_range.split("-")
        low = int(low)
        hi = int(hi)
        for n in range(low, hi+1):
            if is_invalid_p2(n):
                ans += n
    return ans

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))