import os.path

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def HASH(step):
    value = 0
    for c in step:
        ascii = ord(c)
        value += ascii
        value *= 17
        value %= 256
    return value

def part1(data):
    steps = data.strip().split(",")
    s = 0
    for step in steps:
        v = HASH(step)
        s += v
    return s

test = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""
print(part1(test))
print(part1(data))

def part2(data):
    steps = data.strip().split(",")
    boxes = [[] for _ in range(256)]
    for step in steps:
        if "=" in step:
            lens, focal_length = step.split("=")
            focal_length = int(focal_length)
            box = HASH(lens)
            for item in boxes[box]:
                if item[0] == lens:
                    item[1] = focal_length
                    break
            else:
                boxes[box].append([lens, focal_length])
        elif "-" in step:
            lens, _ = step.split("-")
            box = HASH(lens)
            for idx, item in enumerate(boxes[box]):
                if item[0] == lens:
                    del boxes[box][idx]
                    break
    power = 0
    for box, lenses in enumerate(boxes):
        #if lenses:
        #    print(box, lenses)
        for idx, (lens, focal_length) in enumerate(lenses, start=1):
            power += (box + 1 ) * idx * focal_length
    return power

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))