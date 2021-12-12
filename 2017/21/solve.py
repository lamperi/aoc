example = """../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#"""
import os.path
INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read().strip()

def match(square, rule):
    return square == rule

def func(data, iterations):
    start = """.#.
..#
###"""
    rules = {}
    for line in data.splitlines():
        parts = line.split(" => ")

        a = parts[0]
        for rot in range(4):
            a = "/".join(["".join(i) for i in zip(*reversed(a.split("/")))])
            b = "/".join(p[::-1] for p in a.split("/"))

            if a not in rules:
                rules[a] = parts[1]
            if b not in rules:
                rules[b] = parts[1]

    image = start.splitlines()
    for round in range(iterations):
        no_lines = len(image)
        new_image = []
        for size in (2, 3):
            if no_lines % size == 0:
                for i in range(0, no_lines, size):
                    new_lines = [[] for k in range(size+1)]
                    old_lines = [image[k] for k in range(i, i+size)]
                    for j in range(0, no_lines, size):
                        square = "/".join(old_line[j:j+size] for old_line in old_lines)
                        res = rules[square]
                        for new_line, part in zip(new_lines, res.split("/")):
                            new_line.append(part)
                    for new_line in new_lines:
                        new_image.append("".join(new_line))
                image = new_image
                break

    return "\n".join(image).count("#")

print("Test", func(example,2))
print("Part 1",func(data,5))
print("Part 2",func(data,18))
