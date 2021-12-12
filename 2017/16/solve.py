import os.path
INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read().strip()

def transform(status, insts):
    length = len(status)
    for inst in insts:
        if inst[0] == "s":
            size = int(inst[1:]) % length
            status = status[-size:] + status[:-size]
        elif inst[0] == "x":
            parts = inst[1:].split("/")
            parts[0] = int(parts[0])
            parts[1] = int(parts[1])
            status[parts[0]], status[parts[1]] =  status[parts[1]], status[parts[0]]
        elif inst[0] == "p":
            parts = inst[1:].split("/")
            i = status.index(parts[0])
            j = status.index(parts[1])
            status[i], status[j] = status[j], status[i]
    return status

def func1(data, length=16):
    insts = data.split(",")    
    status = []
    for i in range(length):
        status.append(chr(ord('a') + i))
    
    status = transform(status, insts)
    return "".join(status)

        
print(func1("""s1,x3/4,pe/b""", 5), "baedc")
print(func1(data))

def func2(data, length=16, iter=1000000000):
    insts = data.split(",")    
    status = []
    for i in range(length):
        status.append(chr(ord('a') + i))
    
    seen = {}
    for i in range(iter):
        s = "".join(status)
        if s in seen:
            cycle = i - seen[s]
            n = int((iter - seen[s]) / cycle)
            remaining = iter - n*cycle - seen[s];
            for j in range(remaining):
                status = transform(status, insts)
            break
        seen[s] = i
        status = transform(status, insts)
    return "".join(status)

        
print(func2("""s1,x3/4,pe/b""", 5, 2), "ceadb")
print(func2(data))
