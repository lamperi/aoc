import os.path

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()
INPUT = os.path.join(os.path.dirname(__file__), 'test_input.txt')
with open(INPUT) as f:
    test = f.read()

def part1(data):
    m = []
    for line in data.splitlines():
        parts = line.split()
        try:
            parts = [int(p) for p in parts]
        except:
            pass
        m.append(parts)
    total_sum = 0
    for i in range(len(m[0])):
        if m[-1][i] == "+":
            s = 0
            for j in range(0, len(m)-1):
                s += m[j][i]
        else:
            s = 1
            for j in range(0, len(m)-1):
                s *= m[j][i]
        total_sum += s
    return total_sum

print(part1(test))
print(part1(data))

def part2(data):
    lines = data.splitlines()
    column_index = []
    for i, c in enumerate(lines[0]):
        if c == " " and all(l[i] == " " for l in lines):
            column_index.append(i)
    column_index.append(len(lines[0]))
    
    start_index = 0
    total_sum = 0
    for end_index in column_index:
        columns = []
        for line in lines:
            column = line[start_index:end_index]
            columns.append(column)
        
        op = columns[-1][0]
        assert op in "+*"
        
        numbers = []
        for i in range(len(columns[0])):
            digits = 0
            for c in columns[:-1]:
                if c[i] != " ":
                    digits *= 10
                    digits += int(c[i])
            numbers.append(digits)
        if op == "+":
            total_sum += sum(numbers)
        else:
            s = 1
            for n in numbers:
                s *= n
            total_sum += s
        start_index = end_index + 1
    return total_sum                

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))