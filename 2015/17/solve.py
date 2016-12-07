with open("input.txt") as file:
    data = file.read()

import itertools

cans = sorted([int(t) for t in data.splitlines()])

combinations = set()
found = 0
for size in range(len(cans)):
    for subset in itertools.combinations(cans, size):
        if sum(subset) == 150:
            found += 1
            combinations.add(tuple(sorted(subset)))
print("Found {} subsets with sum 150".format(found))

min_size = min(len(comb) for comb in combinations)
print("Found min subset size to be {}".format(min_size))

found = 0
for subset in itertools.combinations(cans, min_size):
    if sum(subset) == 150:
        found += 1
        
print("Found {} minimal subsets with sum 150".format(found))