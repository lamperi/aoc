import os.path

INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

test="""..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
"""

def get_window(image, y, x, d):
    for yd in (-2, -1, 0):
        for xd in (-2, -1, 0):
            yield image.get((y+yd, x+xd), d)

def get_new_pixel(image, y, x, d, enchancement):
    index = 0
    for i, b in enumerate(get_window(image, y, x, d)):
        index |= (b << (8-i))
    return enchancement[index]

def print_map(image, d):
    max_y = max(y for y,_ in image.keys())
    max_x = max(x for _,x in image.keys())
    s = ""
    for y in range(0, max_y):
        for x in range(0, max_x):
            s += "#" if image.get((y,x), d) == 1 else "."
        s+="\n"
    print(s)


def get_lit_pixels(data, t):
    enchancement, image = data.split("\n\n")
    enchancement = [1 if c == "#" else 0 for c in enchancement]
    image = {(y,x): 1 if c == "#" else 0
            for y,line in enumerate(image.splitlines())
            for x, c in enumerate(line)}
    d = 0
    max_y = max(y for y,_ in image.keys()) + 3
    max_x = max(x for _,x in image.keys()) + 3
    for _ in range(t):
        image = {(y,x): get_new_pixel(image, y, x, d, enchancement)
            for y in range(0, max_y)
            for x in range(0, max_x)}
        max_y += 2
        max_x += 2
        # Note: depending on what the 0 value enchancement resolves, we need to 
        # change the default fill value of the infinite image.
        if enchancement[0] == 1:
            d = 1-d

    return sum(image.values())

def part1(data):
    return get_lit_pixels(data, t=2)

print(part1(test))
print(part1(data))

def part2(data):
    return get_lit_pixels(data, t=50)

print(part2(test))
print(part2(data))

