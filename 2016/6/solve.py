import collections

with open("input.txt") as file:
    data = file.read()

strings = []
for line in data.splitlines():
    for i, c in enumerate(line):
        if len(strings) <= i:
            strings.append([])
        strings[i].append(c)

# Part 1
letters = [collections.Counter("".join(s)).most_common()[0][0] for s in strings]
print("".join(letters))

# Part 2
letters = [collections.Counter("".join(s)).most_common()[-1][0] for s in strings]
print("".join(letters))