import os.path

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()
INPUT = os.path.join(os.path.dirname(__file__), 'test_input.txt')
with open(INPUT) as f:
    test = f.read()

def part1(data):
    fresh_ranges_str, available = data.split("\n\n")
    fresh_ranges = []
    for line in fresh_ranges_str.splitlines():
        lo, hi = line.split("-")
        lo = int(lo)
        hi = int(hi)
        fresh_ranges.append((lo, hi))
    available = [int(a) for a in available.splitlines()]
    
    fresh = 0
    for incredient in available:
        for lo, hi in fresh_ranges:
            if lo <= incredient <= hi:
                fresh += 1
                break
    return fresh

print(part1(test))
print(part1(data))

def part2(data):
    fresh_ranges_str, available = data.split("\n\n")
    fresh_ranges = []
    for line in fresh_ranges_str.splitlines():
        lo, hi = line.split("-")
        lo = int(lo)
        hi = int(hi)
        fresh_ranges.append((lo, hi))
        
    # De duplicate ranges
    for j, _ in enumerate(fresh_ranges):
        # Merge into index j as long as there's anything overlapping.
        while True:
            lo, hi = fresh_ranges[j]
            merged = False
            for k, (lo2, hi2) in enumerate(fresh_ranges[j+1:], start=j+1):
                # If the intervals overlap, calculate a new one:
                if lo <= lo2 and hi >= lo2 or lo2 <= lo and hi2 >= lo:
                    new_r = min(lo, lo2), max(hi, hi2)
                    # Put merged interval into index j
                    fresh_ranges[j] = new_r
                    # Delete the unneeded range from index k
                    del fresh_ranges[k]
                    merged = True
                    # Reset loop
                    break
            if not merged:
                break
    # Now that ranges are not overlapping, simple sum works.
    fresh_total = 0
    for lo, hi in fresh_ranges:
        fresh_total += (hi - lo + 1)
    return fresh_total

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))