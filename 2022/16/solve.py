import os.path
from itertools import pairwise
import re

FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(FILE) as f:
    INPUT = f.read()

def ints(line):
    return map(int, re.findall("-?\d+", line))

TEST = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""

def parse_valves(data):
    valves = {}
    for line in data.splitlines():
        if not line.strip():
            continue
        words = line.split()
        id_ = words[1]
        flow_rate = int(words[4].split("=")[1][:-1])
        adj = [w.replace(",", "") for w in words[9:]]
        valves[id_] = (id_, flow_rate, adj)
    return valves

def calculate_optimal_states(valves, max_time):
    states = [
        ('AA', frozenset(), 0),
    ]
    optimal = {}
    pruned = 0
    for t in range(0, max_time):
        new_states = []
        for pos, open_, pressure in states:
            if (pos, open_) in optimal and pressure <= optimal[(pos, open_)]:
                pruned += 1
                continue
            optimal[(pos, open_)] = pressure
            valve_pressure, adj = valves[pos][1:]
            if valve_pressure > 0 and pos not in open_:
                new_states.append((pos, open_ | frozenset([pos]), pressure + valve_pressure * (max_time - t - 1)))
            for a in adj:
                new_states.append((a, open_, pressure))
        states = new_states
    return optimal

def solve(data):
    valves = parse_valves(data)
    states = calculate_optimal_states(valves, 30)
    return max(states.values())

print(solve(TEST))
print(solve(INPUT))

def solve2(data):
    valves = parse_valves(data)
    states = calculate_optimal_states(valves, 26)

    rooms_with_positive_flow = sum(1 for _,f,_ in valves.values() if f > 0)
    # Heuristic: only check states where 1 actor opens up between mi, ma valves (35%..50%)
    mi, ma = 35*rooms_with_positive_flow//100,  5*rooms_with_positive_flow//10
    testable_states = [(s, p) for (_,s),p in states.items() if mi <= len(s) <= ma]
    #print(f"number of testable states {len(testable_states)} of size between {mi} and {ma}")

    max_pressure = 0
    for state,pressure in testable_states:
        for state2,pressure2 in testable_states:
            if len(state & state2) == 0:
                if pressure + pressure2 > max_pressure:
                    max_pressure = max(max_pressure, pressure + pressure2)
                    #print("found better with", len(state), len(state2), max_pressure)
    return max_pressure


print(solve2(TEST))
print(solve2(INPUT))