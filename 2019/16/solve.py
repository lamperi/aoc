with open("input.txt") as f:
    data = f.read().strip()


def pattern2(repeat, k):
    base = 0, 1, 0, -1
    val = int(((k + 1) % ((1+repeat)*4)) / (1+repeat))
    return base[val]

def pattern(n):
    n += 1
    base = 0, 1, 0, -1
    t = 0
    while True:
        for c in base:
            for i in range(n):
                if t > 0:
                    yield c
                t += 1

def fft(input_signal):
    sign = []
    for n in input_signal:
        sign.append(int(n))
    for phase in range(100):
        ns = []
        for j in range(0, len(sign)):
            s = sum(n*p for n, p in zip(sign, pattern(j)))
            ns.append(abs(s) % 10)
        sign = ns
    
    return  "".join(str(i) for i in sign[:8])

def fft2(input_signal, repeat=10000):
    sign = []
    for n in input_signal:
        sign.append(int(n))
    sign *= repeat
    offset = int("".join(str(i) for i in sign[:7]))
    assert offset > len(sign)/2
    sign = sign[offset:]

    for phase in range(100):
        ns = sign[:]
        s = 0
        # Special case: everything before offset is 0, after is 1 in the multiplication table
        for i in range(len(sign), 0, -1):
            s += sign[i-1]
            ns[i-1] = (abs(s) % 10)
        sign = ns
    
    return  "".join(str(i) for i in sign[:8])
    

print(fft("80871224585914546619083218645595"))
print(fft("19617804207202209144916044189917"))
print(fft("69317163492948606335995924319873"))
print(fft(data))

print(fft2("03036732577212944063491565474664"))
print(fft2("02935109699940807407585447034323"))
print(fft2("03081770884921959731165446850517"))
print(fft2(data, 10000))
