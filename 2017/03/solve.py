# Part 1

def func(data):
    w = 0
    h = 0
    x = 0
    y = 0
    d = (0, 0)
    for i in range(data-1):
        if x == w and y == h:
            w += 1
            h += 1
            d = (0, -1)
            x = w
            y = h-1
            continue
        elif x == w and y == -h:
            d = (-1, 0)
        elif x == -w and y == -h:
            d = (0, 1)
        elif x == -w and y == h:
            d = (1, 0)           
        x += d[0]
        y += d[1]
 
    return abs(x) + abs(y)

print(func(1))
print(func(12))
print(func(23))
print(func(1024))
print(func(277678))

# Part 2

def func(data):
    def sum(x, y, v):
        s = 0
        for i in (x-1, x, x+1):
            for j in (y-1, y, y+1):
                s += v.get(i, {}).get(j, 0)
        return s
    w = 0
    h = 0
    x = 0
    y = 0
    d = (0, 0)
    v = {0: {0: 1}}
    for i in range(10*data):
        if x == w and y == h:
            w += 1
            h += 1
            d = (0, -1)
            x = w
            y = h-1
            if x not in v:
                v[x] = {}
            v[x][y] = sum(x, y, v)
            if v[x][y] > data:
                return v[x][y]
            continue
        elif x == w and y == -h:
            d = (-1, 0)
        elif x == -w and y == -h:
            d = (0, 1)
        elif x == -w and y == h:
            d = (1, 0)           
        x += d[0]
        y += d[1]
        if x not in v:
            v[x] = {}
        v[x][y] = sum(x, y, v)
        if v[x][y] > data:
            return v[x][y]

print(func(1))
print(func(12))
print(func(23))
print(func(277678))