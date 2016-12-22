import re, itertools
reg = re.compile(r"/dev/grid/node-x(\d+)-y(\d+) +(\d+)T +(\d+)T +(\d+) +(\d+)%")

"/dev/grid/node-x0-y0     94T   73T    21T   77%"

with open("input.txt") as f:
    data = f.read()

nodes = []
for line in data.splitlines():
    if "/dev/grid" not in line:
        continue
    parts = line.split()
    _,x,y = parts[0].split("-")
    x = int(x[1:])
    y = int(y[1:])
    size = int(parts[1][:-1])
    used = int(parts[2][:-1])
    avail = int(parts[3][:-1])
    usep = int(parts[4][:-1])
    nodes.append((x,y,size,used,avail,usep))

def viable(n1,n2):
    if n1[3] == 0:
        return False
    if n1 == n2:
        return False
    if n1[3] > n2[4]:
        return False
    return True

total = 0
for n1 in nodes:
    for n2 in nodes:
        if viable(n1, n2):
            total += 1

# PART 1:
print(total)

def grid_compat(nodes, t = (-1,-1)):
    p = []
    y = 0
    nodes = [(n[1], n[0], n[2], n[3]) for n in nodes]
    for node in sorted(nodes):
        if node[0] != y:
            y = node[0]
            p.append("\n")
        if node[0] == 0 and node[1] == 0:
            mark = "0"
        elif node[0] == t[1] and node[1] == t[0]:
            mark = "G"
        elif node[3] < 10:
            mark = "_"
        elif node[3] > 100:
            mark = "#"
        else:
            mark = "."
        p.append("{}".format(mark))
    return "".join(p)
                
# PART 2:
            
def solve_simple(nodes, goal):
    G = grid_compat(nodes, goal)
    i = G.index("_")
    queue = [(0, i)]
    distance = None
    neight = [-32,-1,1,32]
    visited = set()
    visited.add(i)
    while queue:
        steps, i = queue[0]
        queue = queue[1:]
        
        l = list(G)
        for v in visited:
            l[v] = "/"
        print("".join(l))
        
        for n in neight:
            j = i+n
            if 0 <= j < len(G) and j%32 != 31 and (j/32 == i/32 or j%32 == i%32): 
                if G[j] == "." and j not in visited:
                    visited.add(j)
                    queue.append((steps+1, j))
                elif G[j] == "G":
                    queue = []
                    distance = steps+1
                    break
    if distance:
        print("BFS found it takes {} steps to carry empty to G and G to (29,0)".format(distance))
        additional = 29 * (1 + 2 + 1 + 1) # down, left, up, right until G is at 0
        print("Since G must be moved still 29 times, total number of moves is {}".format(distance + additional))
        
solve_simple(nodes, (30,0))



    