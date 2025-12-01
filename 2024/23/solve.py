import os.path
from collections import defaultdict
INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def part1(data):
    conns = [a.split("-") for a in data.splitlines()]
    connections = defaultdict(set)
    for a,b in conns:
        connections[a].add(b)
        connections[b].add(a)

    unique_triplets = set()
    for comp, conns in connections.items():
        if not comp.startswith("t"):
            continue
        for x in conns:
            for y in conns:
                if x in connections[y]:
                    triplet = tuple(sorted([comp, x, y]))
                    unique_triplets.add(triplet)

    return len(unique_triplets)

test = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""
print(part1(test))
print(part1(data))

def find_largest(candidates, clique, connections):
    largest = clique
    for i, n in enumerate(candidates):
        if connections[n].issuperset(clique):
            next_clique = clique | set([n])
            next_candidates = candidates[i+1:]
            x = find_largest(next_candidates, next_clique, connections)
            if len(x) > len(largest):
                largest = x            
    return largest

def part2(data):
    conns = [a.split("-") for a in data.splitlines()]
    connections = defaultdict(set)
    for a,b in conns:
        connections[a].add(b)
        connections[b].add(a)

    largest = set()
    seen = set()
    for node in connections.keys():
        candidates = connections[node] - seen
        x = find_largest(sorted(candidates), set([node]), connections)
        seen.add(node)
        if len(x) > len(largest):
            largest = x
    return ",".join(sorted(largest))

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))