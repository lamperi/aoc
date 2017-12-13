import sys, operator, functools, binascii
data = open("input.txt").read().strip()

def func(data):
    inst = []
    for line in data.splitlines():
        p = line.split(": ")
        inst.append([int(p[0]), int(p[1]), 0, 1])
    
    severity = 0
    for i in range(100):
        for firewall in inst:
            if firewall[0] == i and firewall[2] == 0:
                severity += i*firewall[1]
            firewall[2] += firewall[3]
            if firewall[2] == 0:
                firewall[3] = 1
            elif firewall[2] == firewall[1] - 1:
                firewall[3] = -1
    
    return severity
            
        
print(func("""0: 3
1: 2
4: 4
6: 4"""))
print(func(data))

