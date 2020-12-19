import os.path
import collections
import re
import math
import itertools
INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

def match(word, rule, rules, index=0, rule_id=0):
    for or_part in rule:
        new_index = index
        all_match = True
        for p in or_part:
            if p.startswith('"'):
                c = p[1]
                if new_index >= len(word) or word[new_index] != c:
                    all_match = False
                    break
                new_index += 1
            else:
                res, new_index = match(word, rules[int(p)], rules, new_index, int(p))
                if not res:
                    all_match = False
                    break
        if all_match:
            return all_match, new_index
    return False, None

def build_regexp(rule, rules, rule_id=0):
    m = False
    if rule_id == 8 and len(rule) == 2:
        rule = [rule[0]]
        m = True
    if rule_id == 11 and len(rule) == 2:
        rule = [rule[0]]
        m = True

    ret_parts = []
    for or_part in rule:
        inner = []
        for p in or_part:
            if p.startswith('"'):
                c = p[1]
                inner.append(c)
            else:
                reg = build_regexp(rules[int(p)], rules, int(p))
                inner.append(reg)
        if m and rule_id == 11:
            assert len(inner) == 2
            deep_or = []
            for deep in range(1, 10):
                deep_or.append("("+inner[0]+"){" + str(deep) + "}("+inner[1]+"){" + str(deep) + "}")
            ret_parts.append("(" + "|".join(deep_or) + ")")
        else:
            ret_parts.append("".join(inner))

    if m and rule_id == 8:
        assert len(ret_parts) == 1
        return "(" + ret_parts[0]+")+"

    if len(ret_parts) > 1:
        return "(" + "|".join(ret_parts) + ")"
    return ret_parts[0]

def solve(data):
    rules = {}
    words = []
    mode = 1
    for line in data.splitlines():
        if mode == 1:
            if not line:
                mode = 2 
                continue
            id, r = line.split(": ")
            or_parts = [or_part.split() for or_part in r.split(" | ")]
            rules[int(id)] = or_parts
        else:
            words.append(line)

    s = 0
    for word in words:
        ret, index = match(word, rules[0], rules)
        if ret and index == len(word):
            #print("Match", word, index, len(word))
            s += 1
    return s

print(solve("""0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""))
print(solve(data))

def solve_re(data):
    rules = {}
    words = []
    mode = 1
    for line in data.splitlines():
        if mode == 1:
            if not line:
                mode = 2 
                continue
            id, r = line.split(": ")
            or_parts = [or_part.split() for or_part in r.split(" | ")]
            #if id == "8" or id == "11":
            #    print(or_parts)
            rules[int(id)] = or_parts
        else:
            words.append(line)
    reg = build_regexp(rules[0], rules)
    reg = re.compile(reg)
    #print(reg)

    s = 0
    for word in words:
        if re.fullmatch(reg, word):
            #print("Match", word, index, len(word))
            s += 1
    return s

testdata = """42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"""
testdata=testdata.replace("8: 42", "8: 42 | 42 8")
testdata=testdata.replace("11: 42 31", "11: 42 31 | 42 11 31")
print(solve_re(testdata))

data=data.replace("8: 42", "8: 42 | 42 8")
data=data.replace("11: 42 31", "11: 42 31 | 42 11 31")
print(solve_re(data))

