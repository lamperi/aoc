example = """p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>
"""
data = open("input.txt").read()

def sum_vec(v1, v2):
    return [i1+i2 for i1, i2 in zip(v1, v2)]

def func(data):
    partices = []
    for line in data.splitlines():
        parts = line.split(">")[:3]
        p = [int(s.strip()) for s in parts[0].split("<")[1].split(",")]
        v = [int(s.strip()) for s in parts[1].split("<")[1].split(",")]
        a = [int(s.strip()) for s in parts[2].split("<")[1].split(",")]
        partices.append({"p": p, "v": v, "a": a, "d": sum(abs(k) for k in p)})

    for j in range(3000):
        min_p = None
        min_d = None
        for i, particle in enumerate(partices):
            particle["v"] = sum_vec(particle["v"], particle["a"])
            particle["p"] = sum_vec(particle["p"], particle["v"])
            particle["d"] = sum(abs(k) for k in particle["p"])
            if min_d is None or particle["d"] < min_d:
                min_d = particle["d"]
                min_p = i

    return {"Closest to origin": min_p}

print("Test", func(example))
print("Part 1",func(data))

def func(data):
    partices = []
    for line in data.splitlines():
        parts = line.split(">")[:3]
        p = [int(s.strip()) for s in parts[0].split("<")[1].split(",")]
        v = [int(s.strip()) for s in parts[1].split("<")[1].split(",")]
        a = [int(s.strip()) for s in parts[2].split("<")[1].split(",")]
        partices.append({"p": p, "v": v, "a": a, "d": sum(abs(k) for k in p), "alive": True})

    for j in range(3000):
        places = {}
        for i, particle in enumerate(partices):
            if not particle["alive"]:
                continue
            particle["v"] = sum_vec(particle["v"], particle["a"])
            particle["p"] = sum_vec(particle["p"], particle["v"])
            particle["d"] = sum(abs(k) for k in particle["p"])
            pos = tuple(particle["p"])
            if pos not in places:
                places[pos] = []
            places[pos].append(i)

        alive = 0
        for items in places.values():
            if len(items) > 1:
                for item in items:
                    partices[item]["alive"] = False
            else:
                alive += 1

    return {"Still alive": alive}

print("Part 2",func(data))