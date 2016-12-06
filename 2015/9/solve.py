import itertools
import re

with open("input.txt") as file:
    data = file.read()

# PART 1
pattern = r"(\w+) to (\w+) = (\d+)"

edges = []
for (n1,n2,w) in re.findall(pattern, data):
    w = int(w)
    edges.append((n1,n2,w))

# Create adjacency matrix
adj = {}
for n1,n2,w in edges:
    if n1 not in adj:
        adj[n1] = {}
    adj[n1][n2] = w
    if n2 not in adj:
        adj[n2] = {}
    adj[n2][n1] = w

print(adj)

# Traveling salesman, eh, Santa.
cities = set(n1 for n1,n2,w in edges) | set(n2 for n1,n2,w in edges)

# PART 1 & PART 2
def length(state,city):
    if state is None:
        return (city, 0)
    d = adj[state[0]][city]         
    return (city, state[1] + d)

min_path = 10000000
max_path = 0
for perm in itertools.permutations(cities):
    path = reduce(length, perm, None)[1]
    if path > max_path:
        max_path = path
    if path < min_path:
        min_path = path
print(min_path)
print(max_path)