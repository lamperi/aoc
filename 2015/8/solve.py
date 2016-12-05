import re

with open("input.txt") as file:
    data = file.read()

# lazy!
def decode(line):
    return eval(line)

def encode(text):
    replaces = {r'\x': r'\\x',
                r'\"': r'\\\"',
                r'"': r'\"',
                r'\\': r'\\\\'}
    regex = re.compile("|".join(map(re.escape, replaces.keys())))
    return '"' + regex.sub(lambda mo: replaces[mo.group(0)], text) + '"' 

# test
print(encode(r'""'))
print(encode(r'"abc"'))
print(encode(r'"\x27"'))    

# PART 1
total = 0
for line in data.splitlines():
    s = decode(line)
    total += len(line) - len(s)
print(total)


# PART 2

 
total = 0
for line in data.splitlines():
    s = encode(line)
    d = decode(s)
    if line != d:
        print("FAIL!")
        break
    total += len(s) - len(line)
print(total)

