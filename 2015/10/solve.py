data = "1321131112"

def next(s):
    a = []
    cur = None
    count = 0
    for c in s:
        if cur is None:
            cur = c
            count = 1
        elif cur == c:
            count += 1
        else:
            a.append([count,cur])
            cur = c
            count = 1
    if cur:
        a.append([count,cur])
    return "".join(str(j) for t in a for j in t)

# Tests
print(next("1"))
print(next("11"))
print(next("21"))
print(next("1211"))
print(next("111221"))

# Part 1
for i in range(40):
    data = next(data)
print(len(data))

# Part 2
for i in range(10):
    data = next(data)
print(len(data))