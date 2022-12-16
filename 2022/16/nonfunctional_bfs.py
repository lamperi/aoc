def bfs(valves, pos, open_, max_time, current_time):
    q = [(pos, 0)]
    visited = set(pos)
    paths = []
    while q:
        pos, steps = q.pop()
        if pos not in open_ and valves[pos][1] > 0:
            paths.append((pos, steps + 1))
        for a in valves[pos][2]:
            if a not in visited:
                q.append((a, steps + 1))
                visited.add(a)
    # This finds all the non-open producing valves.
    # assert len(open_) + len(paths) == len([v for v in valves if valves[v][1] > 0])
    res = []
    for p, time_to_open in paths:
        time_open = max_time - current_time - time_to_open
        if time_open > 0:
            pressure_released = time_open * valves[p][1]
            res.append((p, time_to_open, pressure_released))
            #print("opening valve", p, "in", time_to_open, "seconds allows to release units", pressure_released, "time left aften opening", time_open)
    return res

def build_adj_graph(valves):
    g = {}
    for k in valves.keys():
        pos = k
        q = [(pos, 0)]
        visited = set(pos)
        paths = []
        while q:
            pos, steps = q.pop()
            if valves[pos][1] > 0:
                paths.append((pos, steps + 1))
            for a in valves[pos][2]:
                if a not in visited:
                    q.append((a, steps + 1))
                    visited.add(a)
        g[k] = paths
    assert g.keys() == valves.keys()
    return g

def adj_from_matrix(g, valves, p, open_, max_time, current_time):
    res = []
    for p, time_to_open in g[p]:
        if p in open_:
            continue
        time_open = max_time - current_time - time_to_open
        if time_open > 0:
            pressure_released = time_open * valves[p][1]
            res.append((p, time_to_open, pressure_released))
            #print("opening valve", p, "in", time_to_open, "seconds allows to release units", pressure_released, "time left aften opening", time_open)
    return res

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

# PART 1
def solve(data, max_time=30):
    valves = parse_valves(data)
    g = build_adj_graph(valves)

    q = [("AA", frozenset(), 0, 0, [])]
    max_pressure = 0
    while q:
        p, open_, total_pressure, t, open_order = q.pop(0)
        if max_pressure < total_pressure:
            max_pressure = total_pressure

        # These are equal:
        # assert bfs(valves, p, open_, max_time, t) == adj_from_matrix(g, valves, p, open_, max_time, t)
        for a, time_to_open, pressure in bfs(valves, p, open_, max_time, t):
            assert t + time_to_open < max_time
            q.append((a, open_ | frozenset([a]), total_pressure + pressure, t + time_to_open, open_order + [(a, t+time_to_open, pressure)]))
    return max_pressure
