with open("input.txt") as f:
    data = f.read().strip()

def get_orbits(i, d):
    return sum(1 + get_orbits(a[0], d) for a in d if a[1] == i)

def solve(d):
    d = [a.split(")") for a in d.splitlines()]
    v = set(a[0] for a in d) | set(a[1] for a in d)
    s = 0
    for i in v:
        s += get_orbits(i, d)
    return s

print(solve("""COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L"""))

# Slow due to recursion
#print(solve(data))

# Directed search for orbits
def solve1(d):
    d = [a.split(")") for a in d.splitlines()]
    v = dict()
    for a,b in d:
        if a not in v:
            v[a] = []
        v[a].append(b)
    l = ["COM"]
    orbits = {}
    orbits["COM"] = 0
    while l:
        node = l[0]
        l = l[1:]
        if node in v:
            for nei in v[node]:
                orbits[nei] = orbits[node] + 1
                l.append(nei)
    return sum(orbits.values())

print(solve1("""COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L"""))

print(solve1(data))

def solve2(d):
    d = [a.split(")") for a in d.splitlines()]
    v = dict()
    for a,b in d:
        if a not in v:
            v[a] = []
        v[a].append(b)
        if b not in v:
            v[b] = []
        v[b].append(a)
    # BFS
    l = ["YOU"]
    visited = set()
    visited.add("YOU")
    length = {}
    length["YOU"] = 0
    while l:
        node = l[0]
        l = l[1:]
        for nei in v[node]:
            if nei in visited:
                continue
            visited.add(nei)
            length[nei] = length[node] + 1
            if nei == "SAN":
                return length[nei] - 2
            l.append(nei)

print(solve2("""COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN"""))

print(solve2(data))