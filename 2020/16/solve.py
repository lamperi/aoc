import os.path
import collections
import re
import math
import itertools
INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()


ranges_re = re.compile(r"([\w ]+): (\d+)-(\d+) or (\d+)-(\d+)")
def solve(data):
    mode = 0
    all_ranges = []
    my = []
    others = []
    for line in data.splitlines():
        if line == "":
            mode += 1
            continue
        if mode == 0:
            m = ranges_re.match(line)
            all_ranges.append((m[1], int(m[2]), int(m[3]), int(m[4]), int(m[5])))
        elif mode == 1:
            if "ticket" in line:
                continue
            my = [int(i) for i in line.split(",")]
        elif mode == 2:
            if "ticket" in line:
                continue
            others.append([int(i) for i in line.split(",")])
    invalid_sum = 0
    valid_tickets = [my]
    for ticket in others:
        all_valid = True
        for n in ticket:
            any_valid = False
            for _, lb1, ub1, lb2, ub2 in all_ranges:
                if lb1 <= n <= ub1 or lb2 <= n <= ub2:
                    any_valid = True
            if not any_valid:
                invalid_sum += n
                all_valid = False
        if all_valid:
            valid_tickets.append(ticket)

    # Solve fields
    valid_per_index = {}
    for index in range(len(valid_tickets[0])):
        valid_per_index[index] = set()
        for fn, lb1, ub1, lb2, ub2 in all_ranges:
            all_valid = all(lb1 <= ticket[index] <= ub1 or lb2 <= ticket[index] <= ub2
              for ticket in valid_tickets)
            if all_valid:
                valid_per_index[index].add(fn)

    # Sort fields by how many possibilies there are.
    valids_optimized = [(len(valids), index, valids) for index, valids in valid_per_index.items()]
    valids_optimized.sort()
    _, fields = search(valids_optimized, set(), set())
    prod = 1
    for index,name in fields.items():
        if name.startswith("departure"):
            prod *= my[index]
    return "P1: {0:5d} P2: {1:15d}".format(invalid_sum, prod)

def search(valids_optimized, used_fields, used_index):
    if len(used_fields) == len(valids_optimized):
        return True, {}
    for _, index, fns in valids_optimized:
        if index in used_index:
            continue
        for fn in fns:
            if fn in used_fields:
                continue
            ret, fields = search(valids_optimized, used_fields | set([fn]), used_index | set([index]))
            if ret == True:
                fields[index] = fn
                return ret, fields
    return False, None
    
print(solve("""class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""))
print(solve(data))