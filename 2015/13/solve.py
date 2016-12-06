with open("input.txt") as file:
    data = file.read()
    
import re
import itertools
    
# Create adjacency matrix
adj = {}
pattern = r"(\w+) would (\w+) (\d+) happiness units by sitting next to (\w+)"
for p1,command,amount,p2 in re.findall(pattern, data):
    if command == "lose":
        amount = -int(amount)
    else: # gain
        amount = int(amount)
        
    if p1 not in adj:
        adj[p1] = {}
    adj[p1][p2] = amount


people = adj.keys()

# PART 1
def length(state,person):
    if state is None:
        return (person, 0)
    h1 = adj[state[0]][person]         
    h2 = adj[person][state[0]]
    return (person, state[1] + h1 + h2)

def solve(people):
    max_happiness = 0
    for perm in itertools.permutations(people):
        perm = perm + (perm[0],)
        happiness = reduce(length, perm, None)[1]
        if happiness > max_happiness:
            max_happiness = happiness
    print(max_happiness)

solve(people)

# PART 2
me = "Toni"
for m in adj.values():
    m[me] = 0
adj[me] = dict((p, 0) for p in people)
people.append(me)

solve(people)