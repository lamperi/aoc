import os.path
import math

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def parse(data):
    inst, graph = data.split("\n\n")
    v = {}
    for line in graph.splitlines():
        source, lr = line.split(" = ")
        left, right = lr.split(", ")
        left = left[1:]
        right = right[:-1]
        assert source not in v
        v[source] = (left, right)
    return inst, v

def run_search(node, inst, v, end_cond):
        i = 0
        while not end_cond(node):
            inst_num = i % len(inst)
            lr = inst[inst_num]
            i += 1
            jump_idx = 0 if lr == "L" else 1
            node = v[node][jump_idx]
        return i

def part1(data):
    inst, v = parse(data)
    return run_search("AAA", inst, v, lambda n: n == "ZZZ")
test = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""
print(part1(test))
print(part1(data))

def part2(data):
    inst, v = parse(data)
    
    nodes = []
    for node in v.keys():
        if node.endswith("A"):
            nodes.append(node)
    
    cycles = []
    for node in nodes:
        cycle = run_search(node, inst, v, lambda n: n.endswith("Z"))
        cycles.append(cycle)

    lcm = 1
    for c in cycles:
        lcm = lcm*c//math.gcd(lcm, c)
    return lcm


# Override test for part 2.
test = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

print(part2(test))
print(part2(data))