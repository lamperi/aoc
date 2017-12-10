import sys, operator, functools
data = open("input.txt").read().strip()

# Shared

def reverse(index, length, value):
    if index+length <= len(value):
        value[index:index+length] = reversed(value[index:index+length])
    else:
        a = length - (len(value) - index)
        rsl = list(reversed(value[index:] + value[:a]))
        value[index:] = rsl[:-a]
        value[:a] = rsl[-a:]

# PART 1

def func(circular_list, inp_list):
    inp_list = [int(p.strip()) for p in inp_list.split(",")]
    skip_size = 0
    index = 0
    for val in inp_list:
        reverse(index, val, circular_list)
        index = (index + val + skip_size) % len(circular_list)
        skip_size += 1
    
    return circular_list[0]*circular_list[1], circular_list
        
print(func(list(range(5)), "3, 4, 1, 5"))
print(func(list(range(256)), data))

# PART 2

def func(inp_list):
    inp_list = [ord(p) for p in inp_list.strip()]
    inp_list += [17, 31, 73, 47, 23]
    circular_list = list(range(256))
    skip_size = 0
    index = 0
    
    for round in range(64):
        for val in inp_list:
            reverse(index, val, circular_list)
            index = (index + val + skip_size) % len(circular_list)
            skip_size += 1
    
    hash_vals = []
    for index in range(0, 256, 16):
        hash_val = functools.reduce(operator.xor, circular_list[index:index+16])
        hash_vals.append(hash_val)
    
    value = "".join([hex(v)[2:] if v >= 16 else "0" + hex(v)[2:] for v in hash_vals])
    return  value    


print(func(""), "a2582a3a0e66e6e86e3812dcb672a272")
print(func("AoC 2017"), "33efeb34ea91902bb2f59c9920caa6cd")
print(func("1,2,3"), "3efbe78a8d82f29979031a4aa0b16a9d")
print(func("1,2,4"), "63960835bcdc130f0b66d7ff4f6a5a8e")
print(func(data), "???")
