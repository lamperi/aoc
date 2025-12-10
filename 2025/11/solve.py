import os.path
from collections import defaultdict, deque

with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as f:
    data = f.read()
with open(os.path.join(os.path.dirname(__file__), 'test_input.txt')) as f:
    test1 = f.read()
with open(os.path.join(os.path.dirname(__file__), 'test_input2.txt')) as f:
    test2 = f.read()

def part1(data):
    graph = {}
    for line in data.splitlines():
        source, dest = line.split(": ")
        dest = dest.split()
        graph[source] = dest

    paths = 0
    stack = deque([("you", 0)])
    while stack:
        cell, steps = stack.pop()
        for n in graph[cell]:
            if n == "out":
                paths += 1
            else:
                stack.append((n, steps+1))
    return paths

print(part1(test1))
print(part1(data))

def part2(data):
    graph = {}
    for line in data.splitlines():
        source, dest = line.split(": ")
        dest = dest.split()
        graph[source] = dest
    
    # Generate the number of reachable nodes from each node.
    reachable_by = {}
    for G in graph.keys():
        visited = set()
        stack = deque([G])
        visited.add(G)
        while stack:
            cell = stack.pop()
            for n in graph.get(cell, []):
                if n in visited:
                    continue
                stack.append(n)
                visited.add(n)
        assert "out" in visited
        reachable_by[G] = visited
    reachable_counts = [(-len(visited), G) for G, visited in reachable_by.items()]
    reachable_counts.sort()

    # Dynamic programming approach:
    # Each path is the sum of path of the previous nodes.
    # This works since there are no cycles in the graph and the nodes are ordered
    # so that we sum them up in the right order.
    paths = defaultdict(int)
    paths["svr"] = 1
    paths_has_fft = defaultdict(int)
    paths_has_dac = defaultdict(int)
    paths_has_dac_fft = defaultdict(int)
    for _, node in reachable_counts:
        for n in graph[node]:
            paths[n] += paths[node]
            paths_has_dac_fft[n] += paths_has_dac_fft[node]
            paths_has_fft[n] += paths_has_fft[node]
            paths_has_dac[n] += paths_has_dac[node]
            if n == "fft":
                paths_has_fft[n] += paths[node]
                paths_has_dac_fft[n] += paths_has_dac[node]
            elif n == "dac":
                paths_has_dac[n] += paths[node]
                paths_has_dac_fft[n] += paths_has_fft[node]

    return paths_has_dac_fft["out"]


print(part2(test2))
print(part2(data))