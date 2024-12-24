import os.path

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

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

swaps = [
    ("z20", "tqq"),
    ("z06", "ksv"),
    ("z39", "ckb"),
    ("nbd", "kbs")
]
#for (a,b) in swaps:
#    operations[a], operations[b] = operations[b], operations[a]

OUTPUT = os.path.join(os.path.dirname(__file__), 'graph.dot')
with open(OUTPUT, "w") as f:
    f.write("digraph graphname {\n")
    for rs, (v1, op, v2) in operations.items():
        f.write(f"  {v1} -> {rs} [label=\"{op}\"]\n")
        f.write(f"  {v2} -> {rs} [label=\"{op}\"]\n")
    f.write("}\n")