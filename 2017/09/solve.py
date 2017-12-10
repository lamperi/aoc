import sys
data = open("input.txt").read().strip()

def func(inp):
    score = 0
    escape = False
    garbage = False
    level = 0
    for c in inp:
        if escape:
            escape = False
            continue
        if garbage and c == "!":
            escape = True
        elif not garbage and c == "<":
            garbage = True
        elif garbage and c == ">":
            garbage = False
        elif not garbage and c == "{":
            level += 1
        elif not garbage and c == "}":
            score += level
            level -= 1
    return score
        


print(func("""{}"""), 1)
print(func("""{{{}}}"""), 6)
print(func("""{{},{}}"""), 5)
print(func("""{{{},{},{{}}}}"""), 16)
print(func("""{<a>,<a>,<a>,<a>}"""), 1)
print(func("""{{<ab>},{<ab>},{<ab>},{<ab>}}"""), 9)
print(func("""{{<!!>},{<!!>},{<!!>},{<!!>}}"""), 9)
print(func("""{{<a!>},{<a!>},{<a!>},{<ab>}}"""), 3)
print(func(data))


def func(inp):
    score = 0
    cancelled = 0
    escape = False
    garbage = False
    level = 0
    for c in inp:
        if escape:
            escape = False
            continue
        if garbage and c == "!":
            escape = True
        elif not garbage and c == "<":
            garbage = True
        elif garbage and c == ">":
            garbage = False
        elif not garbage and c == "{":
            level += 1
        elif not garbage and c == "}":
            score += level
            level -= 1
        elif garbage:
            cancelled += 1
    return cancelled
        


print(func("""<>"""), 0)
print(func("""<random characters>"""), 17)
print(func("""<<<<>"""), 3)
print(func("""<{!>}>"""), 2)
print(func("""<!!>"""), 0)
print(func("""<!!!>>"""), 0)
print(func("""<{o"i!a,<{i<a>"""), 10)
print(func(data))
