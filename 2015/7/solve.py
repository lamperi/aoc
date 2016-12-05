import re
import numpy as np

with open("input.txt") as file:
    data = file.read()

# PART 1
pattern = r"(?:(?:(\w+) )?([A-W]+) )?(\w+) -> (\w+)"
gates = []
for a,op,b,ret in re.findall(pattern, data):
    gates.append((a,op,b,ret))
# Should be as large 
print(len(gates) == len(data.splitlines()))

def wire_all(gates):
    wires = {}
    while gates:
        for a,op,b,ret in gates:
            if ret in wires:
                continue
            #print("{}, {}, {}, {}".format(a, op, b, ret))
            aval = None
            bval = None
            if a and a.isdigit():
                aval = int(a)
            elif a and a in wires:
                aval = wires[a]
            if b and b.isdigit():
                bval = int(b)
            elif b and b in wires:
                bval = wires[b]
            if not a and bval is not None:
                if not op:
                    wires[ret] = bval
                elif op == "NOT":
                    wires[ret] = ~bval
                else:
                    print("Op is '{}'".format(op))
                #print("{} is {}".format(ret, wires[ret]))
                gates.remove((a,op,b,ret)) 
            elif a and aval is not None and bval is not None:
                if op == "AND":
                    wires[ret] = aval & bval
                elif op == "OR":
                    wires[ret] = aval ^ bval
                elif op == "LSHIFT":
                    wires[ret] = aval << bval
                elif op == "RSHIFT":
                    wires[ret] = aval >> bval
                else:
                    print("a = '{}', op is '{}'".format(a, op))
                #print("{} is {}".format(ret, wires[ret]))
                gates.remove((a,op,b,ret))
    return wires["a"]
    
a_signal = wire_all(gates[:])
print(a_signal)

# Part 2: replace b initial input
gates = [(a,op,b,ret) if ret != 'b' else (a,op,str(a_signal),ret) for a,op,b,ret in gates]
a_signal = wire_all(gates[:])
print(a_signal)