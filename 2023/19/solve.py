import os.path

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def parse_input(data):
    workflows_str, ratings_str = data.split("\n\n")
    workflows = {}
    for workflow in workflows_str.splitlines():
        name, rules = workflow[:-1].split("{")
        rules = rules.split(",")
        workflows[name] = []
        for rule in rules:
            if ':' in rule:
                comp, target = rule.rsplit(":")
                if "<" in comp:
                    category, val = comp.split("<")
                    comp = (category, "<", int(val))
                elif ">" in comp:
                    category, val = comp.split(">")
                    comp = (category, ">", int(val))
                else:
                    assert False
            else:
                comp, target = "", rule
            workflows[name].append((comp, target))

    ratings = []
    for rating in ratings_str.splitlines():
        parts = rating[1:-1].split(",")
        rating = []
        for part in parts:
            category, rate = part.split("=")
            rate = int(rate)
            rating.append(rate)
        ratings.append(rating)

    return workflows, ratings

def part1(data):
    workflows, ratings = parse_input(data)

    to_index = {"x": 0, "m": 1, "a": 2, "s": 3}
    total_sum = 0
    for rating in ratings:
        workflow_name = "in"
        while workflow_name not in ("A", "R"):
            workflow = workflows[workflow_name]
            for comp, target in workflow:
                match comp:
                    case a, "<", val:
                        if rating[to_index[a]] < val:
                            workflow_name = target
                            break
                    case a, ">", val:
                        if rating[to_index[a]] > val:
                            workflow_name = target
                            break
                    case "":
                        workflow_name = target
                        break
        if workflow_name == "A":
            total_sum += sum(rating)
    return total_sum

test = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""
print(part1(test))
print(part1(data))

def swap_range(ranges, idx, new_r):
    ranges = list(ranges)
    ranges[idx] = new_r
    return tuple(ranges)

def part2(data):
    workflows, _ = parse_input(data)

    accepted = 0
    rejected = 0
    states = [("in", 0, ((1, 4000), (1, 4000), (1, 4000), (1, 4000)))]
    to_index = {c: index for index, c in enumerate("xmas")}
    while states:
        workflow_name, rule_index, ranges = states.pop(0)
        if workflow_name == "A":
            p = 1
            for r in ranges:
                p *= r[1] - r[0] + 1
            accepted += p
            continue
        elif workflow_name == "R":
            p = 1
            for r in ranges:
                p *= r[1] - r[0] + 1
            rejected += p
            continue
        workflow = workflows[workflow_name]
        comp, target = workflow[rule_index]
        match comp:
            case a, "<", val:
                idx = to_index[a]
                r = ranges[idx]
                if r[0] < val <= r[1]:
                    lower = r[0], val-1
                    upper = val, r[1]
                    states.append((target, 0, swap_range(ranges, idx, lower)))
                    states.append((workflow_name, rule_index+1, swap_range(ranges, idx, upper)))
                else:
                    states.append((workflow_name, rule_index+1, ranges))
            case a, ">", val:
                idx = to_index[a]
                r = ranges[idx]
                if r[0] <= val < r[1]:
                    lower = r[0], val
                    upper = val+1, r[1]
                    states.append((workflow_name, rule_index+1, swap_range(ranges, idx, lower)))
                    states.append((target, 0, swap_range(ranges, idx, upper)))
                else:
                    states.append((workflow_name, rule_index+1, ranges))
            case "":
                states.append((target, 0, ranges))
    assert accepted + rejected == 4000**4
    return accepted

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))