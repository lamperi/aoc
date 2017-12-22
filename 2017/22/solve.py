example = """..#
#..
..."""
data = open("input.txt").read()

def func(inp, iterations, size=21):
    data = [['.' for b in range(size)] for a in range(size)]
    offset = int((size - len(inp.splitlines()))/2)
    for i, line in enumerate(inp.splitlines()):
        for j, c in enumerate(line):
            data[i+offset][j+offset] = c

    pos = complex(int(size/2), int(size/2))
    dir = 0 - 1j

    inf = 0
    for round in range(iterations):
        if data[int(pos.imag)][int(pos.real)] == ".":
            dir *= -1j
            data[int(pos.imag)][int(pos.real)] = "#"
            pos += dir
            inf += 1
        else:
            dir *= 1j
            data[int(pos.imag)][int(pos.real)] = "."
            pos += dir

    return inf


print("Test (5587)   :", func(example, 70, 11))
print("Part 1        :", func(data, 10000, 501))

def func(inp, iterations, size=21):
    data = [['.' for b in range(size)] for a in range(size)]
    offset = int((size - len(inp.splitlines()))/2)
    for i, line in enumerate(inp.splitlines()):
        for j, c in enumerate(line):
            data[i+offset][j+offset] = c

    pos = complex(int(size/2), int(size/2))
    dir = 0 - 1j

    inf = 0
    for round in range(iterations):
        state = data[int(pos.imag)][int(pos.real)]
        if state == ".":
            dir *= -1j
            data[int(pos.imag)][int(pos.real)] = "W"
            pos += dir
        elif state == 'W':
            #dir *= 1j
            data[int(pos.imag)][int(pos.real)] = "#"
            pos += dir
            inf += 1
        elif state == '#':
            dir *= 1j
            data[int(pos.imag)][int(pos.real)] = "F"
            pos += dir
        elif state == 'F':
            dir *= -1
            data[int(pos.imag)][int(pos.real)] = "."
            pos += dir

    return inf

print("Test (26)     :", func(example, 100, 11))
print("Test (2511944):", func(example, 10000000, 1001))
print("Part 2        :", func(data, 10000000, 1001))
