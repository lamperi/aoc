import os.path
INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read().strip()

def func(data):
    inst = []
    for line in data.splitlines():
        p = line.split(": ")
        inst.append([int(p[0]), int(p[1]), 0, 1])

    runs = []
    delay = 0
    while True:
        if delay%1000 == 0:
            print(delay)
        runs.append([delay, 0])
        
        new_runs = []
        for run in runs:
            for firewall in inst:
                if firewall[0] == run[1] and firewall[2] == 0:
                    break
            else:
                run[1] += 1
                new_runs.append(run)
                if run[1] == 100:
                    return run[0]
        runs = new_runs

        for firewall in inst:
            
            firewall[2] += firewall[3]
            if firewall[2] == 0:
                firewall[3] = 1
            elif firewall[2] == firewall[1] - 1:
                firewall[3] = -1
                
        delay += 1
    
        
print(func(data))

