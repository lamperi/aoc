example = """../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#"""
data = open("input.txt").read()

def match(square, rule):
    return square == rule

def func(data, iter):
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
    for round in range(iter):
        no_lines = len(image)
        new_image = []
        if no_lines % 2 == 0:
            for i in range(0, no_lines, 2):
                new_line1 = []
                new_line2 = []
                new_line3 = []
                line1 = image[i]
                line2 = image[i+1]
                for j in range(0, no_lines, 2):
                    square = line1[j:j+2] + "/" + line2[j:j+2]
                    res = rules[square]
                    p = res.split("/")
                    new_line1.append(p[0])
                    new_line2.append(p[1])
                    new_line3.append(p[2])
                new_image.append("".join(new_line1))
                new_image.append("".join(new_line2))
                new_image.append("".join(new_line3))
            image = new_image

        elif no_lines % 3 == 0:
            for i in range(0, no_lines, 3):
                new_line1 = []
                new_line2 = []
                new_line3 = []
                new_line4 = []
                line1 = image[i]
                line2 = image[i+1]
                line3 = image[i+2]
                for j in range(0, no_lines, 3):
                    square = line1[j:j+3] + "/" + line2[j:j+3] + "/" + line3[j:j+3]
                    res = rules[square]
                    p = res.split("/")
                    new_line1.append(p[0])
                    new_line2.append(p[1])
                    new_line3.append(p[2])
                    new_line4.append(p[3])
                new_image.append("".join(new_line1))
                new_image.append("".join(new_line2))
                new_image.append("".join(new_line3))
                new_image.append("".join(new_line4))
            image = new_image

    return "\n".join(image).count("#")

print("Test", func(example,2))
print("Part 1",func(data,5))
print("Part 2",func(data,18))
