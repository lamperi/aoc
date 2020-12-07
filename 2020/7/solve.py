import os.path
import collections
import re
import math
INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

def solve(data):
    e = {}
    e2 = {}
    for line in data.split("\n"):
        if not line:
            continue
        bag_type, b = line.split(" contain ")
        bag_type = " ".join(bag_type.split()[:2])
        parts = b.split(", ")
        for p in parts:
            count, bag = p.split(None, 1)
            bag = " ".join(bag.split()[:2])
            if not bag in e:
                e[bag] = []
            e[bag].append(bag_type)
            if count == "no":
                continue
            if not bag_type in e2:
                e2[bag_type] = []
            e2[bag_type].append((int(count), bag))
    t = ["shiny gold"]
    v = set(t)
    while t:
        cur = t.pop()
        if cur not in e:
            continue
        for b in e[cur]:
            if not b in v:
                v.add(b)
                t.append(b)
    s1 = len(v)-1

    t = [(1, "shiny gold")]
    v = set(["shiny gold"])
    s2 = 0
    while t:
        mul, cur = t.pop()
        if cur not in e2:
            continue
        for count, b in e2[cur]:
            s2 += mul*count
            v.add(b)
            t.append((mul*count, b))
    return s1, s2

print(solve("""light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""))
print(solve(data))
