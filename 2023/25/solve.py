import os.path
import itertools
import collections
import networkx as nx
import random

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def bfs(edges, s, t=None, cut=frozenset()):
    queue = collections.deque([s])
    visited = set(queue)
    parent = {}
    while queue:
        node = queue.popleft()
        for adj in edges[node]:
            if (node, adj) in cut or (adj, node) in cut:
                continue
            if adj in visited:
                continue
            queue.append(adj)
            visited.add(adj)
            parent[adj] = node
            if node == t:
                queue.clear()
                break
    return visited, parent

def probalistic_method(edges):
    nodes = list(edges.keys())
    trials = len(nodes) * 5
    done_trial = set()
    used_edge = collections.Counter()
    while len(done_trial) < trials:
        s, t = random.sample(nodes, 2)
        if (s, t) in done_trial or (t, s) in done_trial:
            continue
        done_trial.add((s, t))
        success, parent = bfs(edges, s, t=t)
        assert success
        n = t
        while n != s:
            nn = parent[n]
            a, b = sorted((n, nn))
            used_edge[(a, b)] += 1
            n = nn
    mc = used_edge.most_common(3)
    return [e for e, _ in mc]

def part1(data):
    components = {}
    for line in data.splitlines():
        s, t = line.split(": ")
        t = t.split()
        components[s] = t
    
    all_conns = []
    inv = collections.defaultdict(list)
    for s, t in components.items():
        for tt in t:
            all_conns.append((s, tt))
            inv[tt].append(s)
    
    all_edges = collections.defaultdict(list)
    for v, adj in itertools.chain(components.items(), inv.items()):
        all_edges[v].extend(adj) 

    ec = probalistic_method(all_edges)

    all_nodes = set(components.keys()) | set(inv.keys())
    node = next(iter(all_nodes))
    visited, _ = bfs(all_edges, node, cut=ec)
    assert len(visited) < len(all_nodes), "Probalistic method failed to find correct edges to remove."
    node = next(n for n in all_nodes if n not in visited)
    visited2, _ = bfs(all_edges, node, cut=ec)
    assert len(visited & visited2) == 0
    assert len(visited | visited2) == len(all_nodes)
    return len(visited) * len(visited2)

test = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""
print(ans := part1(test))
assert ans == 54
print(part1(data))
