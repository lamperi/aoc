import sys, operator, functools, binascii
data = open("input.txt").read().strip()

def func(data):
    inst = []
    for line in data.splitlines():
        p = line.split(" <-> ")
        id = int(p[0])
        comms = [int(a) for a in p[1].split(", ")]
        inst.append([id, comms])
    groups = []
    
    for id, comms in inst:
        added = False
        for group in groups:
            if id in group:
                added = True
                for comm in comms:
                    group.add(comm)
        if not added:
            new_group = set()
            new_group.add(id)
            for comm in comms:
                new_group.add(comm)
            groups.append(new_group)
            
    # merging
    def merge(groups):
        for i, a in enumerate(groups):
            for j, b in enumerate(groups[i+1:], i+1):
                if a & b:
                    print("Merge",i,a,j,b)
                    new_set = a | b
                    groups[i] = new_set
                    del groups[j]
                    return True
        return False
    
    while True:
        m = merge(groups)
        if not m: 
            break
            
            
    # Part 1, part 2
    return len(groups[0]), len(groups)
        
        
print(func("""0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5"""))
print(func(data))

