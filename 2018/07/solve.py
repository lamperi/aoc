data = open("input.txt").read().strip()

import re
import string
from collections import Counter

example = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""

def solve1(data):
    rel = []
    nodes = set()
    for line in data.splitlines():
        p = line.split()
        a, b = p[1], p[7]
        rel.append((a,b))
        nodes.add(a)
        nodes.add(b)
    

    roots = nodes - set(c for p, c in rel)
    available = sorted(list(roots))

    o = []
    while available:
        current = available[0]
        available = available[1:]
        if current in o:
            continue
        o.append(current)
        nexts = [c for p, c in rel if p == current]
        for n in nexts:
            prev = [p for p, c in rel if c == n]
            #print("prev", prev, n)
            if all(p in o for p in prev):
                available = available + [n]
        available = sorted(available)

    ret = ''.join(o)
    return ret

print(solve1(example))
print(solve1(data))

def solve2(data, n_workers, duration):
    rel = []
    nodes = set()
    for line in data.splitlines():
        p = line.split()
        a, b = p[1], p[7]
        rel.append((a,b))
        nodes.add(a)
        nodes.add(b)
    
    roots = nodes - set(c for p, c in rel)
    available = sorted(list(roots))

    t = 0
    o = []
    workers = [None] * n_workers
    while True:
        for i, worker in enumerate(workers):
            if worker is not None:
                if worker[1] == 0:
                    completed_job = worker[0]
                    o.append(completed_job)
                    workers[i] = None

                    nexts = [c for p, c in rel if p == completed_job]
                    for n in nexts:
                        prev = [p for p, c in rel if c == n]
                        if all(p in o for p in prev):
                            available = available + [n]
                    available = sorted(available)
                    if not available:
                        if all(w is None for w in workers):
                            assert(len(o) == len(nodes))
                            return t
                else:
                    workers[i] = (worker[0], worker[1]-1)
        for i, worker in enumerate(workers):
            if worker is None and available:
                job = available[0]
                available = available[1:]
                workers[i] = (job, duration + (ord(job) - ord('A')))

        #print('\t'.join([str(t)] + [p[0] if p is not None else '.' for p in workers] + [''.join(o)]))
        t += 1

print(solve2(example, 2, 0))
print(solve2(data, 5, 60))