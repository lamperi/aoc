import os.path
from itertools import combinations, permutations
from random import randint

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def run_prog(vals, operations):
    changed = True
    while changed:
        changed = False
        for res, (v1, op, v2) in operations.items():
            #print(res, v1, v2, res in vals, v1 in vals, v2 in vals)
            if res not in vals and v1 in vals and v2 in vals:
                match op:
                    case "AND": vals[res] = vals[v1] & vals[v2]
                    case "OR": vals[res] = vals[v1] | vals[v2]
                    case "XOR": vals[res] = vals[v1] ^ vals[v2]
                changed = True
                break
    return vals

def part1(data):
    values, gates = data.split("\n\n")

    vals = {}
    for v in values.splitlines():
        reg, val = v.split()
        val = int(val)
        vals[reg[:-1]] = val

    operations = {}
    for gate in gates.splitlines():
        v1, op, v2, _, rs = gate.split()
        operations[rs] = (v1, op, v2)

    run_prog(vals, operations)

    z_keys = sorted([k for k in operations.keys() if k.startswith("z")])
    return sum(vals.get(k, 0) << i for i, k in enumerate(z_keys))
test = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""
print(part1(test))
print(part1(data))

def find_broken_bit(z_keys, bit_size, operations):
    min_zeros = len(z_keys)
    for n in range(20):
        rand_x = randint(0, 1 << bit_size - 1)
        rand_y = randint(0, 1 << bit_size - 1)
        regs = {}
        for b in range(0, bit_size + 1):
            regs[f"x{b:02}"] = (rand_x >> b) & 1
            regs[f"y{b:02}"] = (rand_y >> b) & 1
        run_prog(regs, operations)
        z = sum(regs.get(k, 0) << i for i, k in enumerate(z_keys))
        diff = z ^ (rand_x + rand_y)
        if diff != 0:
            zeros = 0
            while diff != 0 and diff & 1 == 0:
                zeros += 1
                diff >>= 1
            min_zeros = min(zeros, min_zeros)
    return min_zeros

def find_relevant_nodes(operations, bit):
    relevant_nodes = set()
    x = f"x{bit:02}"
    y = f"y{bit:02}" 
    z = f"z{bit:02}"

    for rs, (v1, _op, v2) in operations.items():
        if x in (v1, v2) or y in (v1, v2):
            relevant_nodes.add(rs)
        if rs == z:
            relevant_nodes.add(rs)
    more_relevant = []
    for rs, (v1, _op, v2) in operations.items():
        for n in relevant_nodes:
            if n in (v1, v2):
                more_relevant.append(rs)
    relevant_nodes.update(more_relevant)
    return relevant_nodes

def part2(data):
    values, gates = data.split("\n\n")
    vals = {}
    for v in values.splitlines():
        reg, val = v.split()
        val = int(val)
        vals[reg[:-1]] = val
    bit_size = len(vals)//2
    operations = {}
    for gate in gates.splitlines():
        v1, op, v2, _, rs = gate.split()
        operations[rs] = (v1, op, v2)
    z_keys = sorted([k for k in operations.keys() if k.startswith("z")])

    swapped_nodes = []
    for _ in range(4):
        min_zeros = find_broken_bit(z_keys, bit_size, operations)
        relevant_nodes = find_relevant_nodes(operations, min_zeros)
        # print("anomaly around", min_zeros)
        # print("relevant nodes", relevant_nodes)

        # try to swap the two nodes
        possible_swap = []
        for (a,b) in combinations(relevant_nodes, 2):
            operations_copy = operations.copy()
            operations_copy[a], operations_copy[b] = operations_copy[b], operations_copy[a]

            bb = find_broken_bit(z_keys, bit_size, operations_copy)
            if bb > min_zeros + 1:
                possible_swap = [(a,b, operations_copy, bb)]
        assert len(possible_swap) == 1, f"Need to find one swap, found {len(possible_swap)}"
        a,b,operations,min_zeros = possible_swap[0]
        swapped_nodes.append(a)
        swapped_nodes.append(b)
        # print("swap", a, b)

    return ",".join(sorted(swapped_nodes))

print(part2(data))