import sys
data = sys.stdin.read()


def rotate(c, shift):
    if c == "-":
        return " "
    index = ord(c) - ord("a")
    solved = (index + shift) % 26
    ret = chr(solved + ord("a"))
    return ret 

def decrypt(encrypted, sector):
    return "".join(rotate(a, sector) for a in encrypted)

def calc_checksum(encrypted):
    e = sorted(encrypted.replace("-", ""))
    m = {}
    for a in e:
        if a in m:
            m[a] += 1
        else:
            m[a] = 1
    b = sorted([(-v,k) for k,v in m.items()])[:5]
    return "".join(t[1] for t in b)
    

total = 0
for line in data.splitlines():
    encrypted, rest = line.rsplit("-", 1)
    sector, rest = rest.split("[")
    checksum = rest.split("]")[0]
    c = calc_checksum(encrypted)
    if c == checksum:
        total += int(sector)

    plain = decrypt(encrypted, int(sector))
    if "north" in plain and "pole" in plain:
        print(encrypted + " " + plain + " " + sector)
    
print(total)
