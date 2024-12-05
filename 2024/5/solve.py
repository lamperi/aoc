import os.path
import functools

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def is_valid(update, rules):
    seen = set()
    for n in update:
        for k, v in rules:
            if k == n:
                if v in seen:
                    return False
        seen.add(n)
    return True


def part1(data):
    rules,updates = data.split("\n\n")
    rules = [rule.split("|") for rule in rules.splitlines()]
    rules = [(int(k), int(v)) for (k,v) in rules]
    updates = [list(map(int, update.split(","))) for update in updates.splitlines()]
    
    s = 0
    for update in updates:
        if is_valid(update, rules):
            m = len(update)//2
            s += update[m]
    return s

test = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""
print(part1(test))
print(part1(data))

def order_updates(update, rules):
    total_ordering = {}
    for (a,b) in rules:
        if a not in update or b not in update:
            continue

        if a not in total_ordering:
            total_ordering[a] = set()
        if b not in total_ordering:
            total_ordering[b] = set()
        total_ordering[a].add(b)
    for _ in range(len(total_ordering)):
        for k, v in total_ordering.items():
            for smaller in list(v):
                v |= total_ordering[smaller]

    
    def compare(x, y):
        if y in total_ordering[x]:
            assert x not in total_ordering[y]
            return -1
        elif x in total_ordering[y]:
            assert y not in total_ordering[x]
            return 1
        else:
            assert False
    #print("update first", update)
    update.sort(key=functools.cmp_to_key(compare))
    #print("update then", update)


def part2(data):
    rules,updates = data.split("\n\n")
    rules = [rule.split("|") for rule in rules.splitlines()]
    rules = [(int(k), int(v)) for (k,v) in rules]
    updates = [list(map(int, update.split(","))) for update in updates.splitlines()]
        
    s = 0
    for update in updates:
        if not is_valid(update, rules):
            order_updates(update, rules)
            m = len(update)//2
            s += update[m]
            assert is_valid(update, rules)
                    
    return s

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))