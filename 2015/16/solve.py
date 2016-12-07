with open("input.txt") as file:
    data = file.read()
    
import re
import itertools

target_props = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1    
}

def m(k, v):
    if k in ("cats", "trees"):
        return target_props[k] < v
    elif k in ("pomeranians", "goldfish"): 
        return target_props[k] > v
    return target_props[k] == v

aunts = []
pattern = r"Sue (\d+): (\w+): (\d+), (\w+): (\d+), (\w+): (\d+)"
for id, prop1, val1, prop2, val2, prop3, val3 in re.findall(pattern, data):
    
    val1 = int(val1)
    val2 = int(val2)
    val3 = int(val3)
    props = {prop1: val1, prop2: val2, prop3: val3}
    match = all(target_props[k] == v for k,v in props.items())
    if match:
        print("PART 1: Aunt {} matches".format(id))
    match = all(m(k,v) for k,v in props.items())
    if match:
        print("PART 2: Aunt {} matches".format(id)) 
