example = 3
data = 314

def func1(data):
    buf = [0]
    current_pos = 0

    for i in range(2017):
        current_pos = (current_pos + data) % len(buf)
        buf.insert(current_pos+1, i+1)
        current_pos += 1

    return buf[(current_pos + 1) % len(buf)]

print(func1(example))
print(func1(data))

def func2(data):
    current_pos = 0

    buf_length = 1
    zero_pos = 0
    after_zero = None

    for i in range(50000000):
        current_pos = (current_pos + data) % buf_length
        if current_pos == zero_pos:
            after_zero = i+1
        elif current_pos < zero_pos:
            zero_pos += 1
        current_pos += 1
        buf_length += 1

    return after_zero

print(func2(data))