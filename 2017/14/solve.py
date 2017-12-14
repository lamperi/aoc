import sys, operator, functools, binascii
data = "vbqugkhl"

def reverse(index, length, value):
    if index+length <= len(value):
        value[index:index+length] = reversed(value[index:index+length])
    else:
        a = length - (len(value) - index)
        rsl = list(reversed(value[index:] + value[:a]))
        value[index:] = rsl[:-a]
        value[:a] = rsl[-a:]

def knot(inp_list):
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
    
    value = binascii.hexlify(bytes(hash_vals))
    return  value    


def func(data):
    coun = 0
    for line in range(128):
        inp = data + "-" + str(line)
        hexed = knot(inp)
        byte_seq = binascii.unhexlify(hexed)

        for c in byte_seq:
            b = (bin(c)[2:])
            coun += sum(1 for a in b if a == "1")
    
    return coun
        
print(func("""flqrgnkx"""), 8108)
print(func(data))

def bfs(grid, i, j):
    q = [(i, j)]
    while q:
        i, j = q[0]
        q = q[1:]
        grid[i][j] = "2"
        for neigh in ((i-1, j), (i, j-1), (i+1, j), (i, j+1)):
            if 0 <= neigh[0] < 128 and 0 <= neigh[1] < 128 and grid[neigh[0]][neigh[1]] == "1":
                q.append(neigh)
    

def func(data):
    grid = []
    coun = 0
    for line in range(128):
        inp = data + "-" + str(line)
        hexed = knot(inp)
        byte_seq = binascii.unhexlify(hexed)

        row = []
        for c in byte_seq:            
            b = (bin(c)[2:])
            b = ("0"*(8-len(b))) + b
            row.append(b)
        grid.append("".join(row))
    
    grid =  "\n".join(grid)
    
    # Find connected parts
    grid = [[c for c in line.strip()] for line in grid.splitlines()]
    
    regions = 0
    for i in range(128):
        for j in range(128):
            if grid[i][j] == "1":
                bfs(grid, i, j)
                regions += 1
    return regions
        
print(func("""flqrgnkx"""), 1242)
print(func(data))

