with open("input.txt") as file:
    data = file.read()
    
import re
import itertools

replacements = []
pattern = r"(\w+) => (\w+)"
for replacement_from, replacement_to in re.findall(pattern, data):
    replacements += [(replacement_from, replacement_to)]

# Get "best" replacements first
replacements.sort(key=lambda r: -len(r[1]))



# PART 1
res = set()    

inp = data.splitlines()[-1]
for replacement in replacements:
    src = replacement[0]
    dst = replacement[1]
    for idx in [m.start() for m in re.finditer(src, inp)]:
        mole = inp[:idx] + dst + inp[idx+len(src):]
        res.add(mole)
        
print(len(res)) 

# PART 2

# Make all unique symbols one letter long (this'll help us later)
# Left open mark
data = data.replace("Rn", "L")
# Deliminator
data = data.replace("Y", " ")
# Right close mark
data = data.replace("Ar", "R")
# Avoid clash with Ti
data = data.replace("Th", "U")
# Remove random small letters - just keep 'e'
data = data.replace("a", "")
data = data.replace("l", "")
data = data.replace("i", "")
data = data.replace("g", "")
print(data)

inp = data.splitlines()[-1].strip()

def solve2(word):
    stack = [-1]
    for c in word:
        if c == 'L':
            stack.append(0)
        elif c == 'R':
            v = stack.pop()
            stack[-1] += v
        elif c == ' ':
            stack[-1] -= 1
        else:
            stack[-1] += 1
    if len(stack) > 1:
        raise Exception("Unbalanced")
    return stack[-1]

print("2 = {}".format(solve2("OBF")))
print("1 = {}".format(solve2("HF")))
print("1 = {}".format(solve2("NLFR")))
print("1 = {}".format(solve2("CLF FR")))
print("1 = {}".format(solve2("CLF F FR")))
print("2 = {}".format(solve2("CLF BFR")))
print("3 = {}".format(solve2("CCLF BFR")))
print("6 = {}".format(solve2("SLCSLTLFRSARR")))
print("21 = {}".format(solve2("SLCSLTLFRSARPTBPTLCSARCPTTBPM FR")))
print("? = {}".format(solve2(inp)))
