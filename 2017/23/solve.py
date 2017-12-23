example = """"""
data = open("input.txt").read()

def val(var, reg):
    try:
        return int(var)
    except:
        return reg.get(var, 0)

def execute(insts, reg, ptr):
    if 0 <= ptr < len(insts):
        inst = insts[ptr]
        if inst[0] == "set":
            reg[inst[1]] = val(inst[2], reg)
        elif inst[0] == "add":
            reg[inst[1]] = reg.get(inst[1], 0) + val(inst[2], reg)
        elif inst[0] == "sub":
            reg[inst[1]] = reg.get(inst[1], 0) - val(inst[2], reg)
        elif inst[0] == "mul":
            reg[inst[1]] = reg.get(inst[1], 0) * val(inst[2], reg)
        elif inst[0] == "mod":
            reg[inst[1]] = reg.get(inst[1], 0) % val(inst[2], reg)
        elif inst[0] == "jnz":
            if val(inst[1], reg) != 0:
                ptr += val(inst[2], reg)
            else:
                ptr += 1
        else:
            print("Apua", inst[0])
        if inst[0] != "jnz":
            ptr += 1
    return ptr

def primes_sieve(limit):
    a = [True] * limit
    a[0] = a[1] = False

    for (i, isprime) in enumerate(a):
        if isprime:
            yield i
            for n in range(i*i, limit, i):
                a[n] = False

primes = list(primes_sieve(123701))

def is_prime(number):
    return number in primes

def func(data, **initial_values):

    insts = []
    reg={}
    reg.update(initial_values)
    ptr = 0
    for line in data.splitlines():
        insts.append(line.split())

    mul_used = 0
    while 0 <= ptr < len(insts):
        if initial_values and ptr == 10:
            # Cheat on prime detection instructions...
            reg['d'] = reg['b']
            reg['g'] = 0
            if not is_prime(reg['b']):
                reg['f'] = 0
            ptr = 23
            continue
        if insts[ptr][0] == "mul":
            mul_used += 1
        ptr = execute(insts, reg, ptr)

    return mul_used, reg.get('h', None)

print("Part 1        :", func(data)[0])
print("Part 2        :", func(data, a=1)[1])

