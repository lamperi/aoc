import os.path
INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read().strip()

def new_conf(conf):
    m = max(conf)
    max_i = conf.index(m)
    conf[max_i] = 0
    for i in range(m):
        conf[(1+i+max_i) % len(conf)] += 1
    
    return conf

# Part 1

def func(data):
    # multiple numbers per line:
    conf = [[int(word) for word in line.split()] for line in data.splitlines()][0]
    seen = set()
    
    while True:
        conf_s = ",".join(str(c) for c in conf)
        if conf_s in seen:
            return len(seen)
        else:
            seen.add(conf_s)
            conf = new_conf(conf)

print(func("0 2 7 0"))
print(func(data))

# Part 2

def func(data):
    # multiple numbers per line:
    conf = [[int(word) for word in line.split()] for line in data.splitlines()][0]
    seen = set()
    
    while True:
        conf_s = ",".join(str(c) for c in conf)
        if conf_s in seen:
            s = 0
            target = conf_s
            while True:
                conf = new_conf(conf)
                conf_s = ",".join(str(c) for c in conf)
                s += 1
                if conf_s == target:
                    return s

        else:
            seen.add(conf_s)
            conf = new_conf(conf)

print(func("0 2 7 0"))
print(func(data))
