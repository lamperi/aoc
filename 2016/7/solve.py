import collections
import re

with open("input.txt") as file:
    data = file.read()

pattern = r"((.)(.)\2\3)"

def check(line):
    m = False
    l = len(line)
    warn = False
    for i in range(l-3):
        if line[i] == "[":
            warn = True
            continue
        elif line[i] == "]":
            warn = False
            continue
        if line[i] == line[i+3] and line[i+1] == line[i+2] and line[i] != line[i+1]:
            m = True
            if warn:
                return False
            #if (i  > 0 and line[i-1] == "[") and (i < l-3 and line[i+4] == "]"):
            #    return False
 
    
    return m

def check_ssl(line):
    m = False
    l = len(line)
    warn = False
    babs = set()
    abas = set()
    for i in range(l-2):
        if line[i] == "[":
            warn = True
            continue
        elif line[i] == "]":
            warn = False
            continue
        if line[i] == line[i+2] and line[i] != line[i+1]:
            m = True
            if warn:
                bab = line[i:i+2]
                babs.add(bab)
            else:
                aba = line[i+1:i+3]
                abas.add(aba)
    
    return len(babs & abas) > 0

    
print(check("abba[mnop]qrst"))
print(check("abcd[bddb]xyyx"))
print(check("aaaa[qwer]tyui"))
print(check("ioxxoj[asdfgh]zxcvbn"))

count = 0
for line in data.splitlines():
    if check(line):
        count += 1
print(count)

print(check_ssl("aba[bab]xyz"))
print(check_ssl("xyx[xyx]xyx"))
print(check_ssl("aaa[kek]eke"))
print(check_ssl("zazbz[bzb]cdb"))

count = 0
for line in data.splitlines():
    if check_ssl(line):
        count += 1
print(count)