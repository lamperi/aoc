data = open('input.txt').read()
example = """^ENWWW(NEEE|SSE(EE|N))$"""
from collections import defaultdict, deque
from heapq import heappop, heappush

def n(edges, y, x):
    for edge in edges[(y, x)]:
        yield edge

def parse_regex(input_data):
    print("Parse regex")
    queue = deque([(0,0,0,deque([]))]) # y, x, start_i, stack copy
    edges = defaultdict(list)
    while queue:
        y, x, start_i, stack = queue.popleft()
        for i, c in enumerate(input_data[start_i:], start_i):
            if c in "^$":
                if c == '$':
                    assert len(stack) == 0
            elif c in 'NEWS':
                dy, dx = {'N': (-1, 0), 'E': (0, 1), 'W': (0, -1), 'S': (1, 0)}[c]
                edges[(y,x)].append((dy+y, dx+x))
                edges[(dy+y,dx+x)].append((y, x))
                y, x = dy+y, dx+x
            elif c == '(':
                stack.append((y, x))
            elif c == ')':
                y, x = stack.pop()
            elif c == '|':
                y, x = stack[-1]
                queue.append((y, x, i+1, stack.copy()))
            else:
                assert False
    return edges

def parse_regex2(input_data):
    edges = defaultdict(list)

    stack = []
    current_starts = {(0, 0)}
    current_ends = set()
    current_position = [(0, 0)]
    for c in input_data:
        if c in "^$":
            if c == '$':
                assert len(stack) == 0
        elif c in 'NEWS':
            dy, dx = {'N': (-1, 0), 'E': (0, 1), 'W': (0, -1), 'S': (1, 0)}[c]
            new_pos = set()
            for y, x in current_position:
                edges[(y,x)].append((dy+y, dx+x))
                edges[(dy+y,dx+x)].append((y, x))
                new_pos.add((dy+y, dx+x))
            current_position = new_pos
        elif c == '(':
            stack.append((current_starts, current_ends))
            current_starts, current_ends = current_position, set()
        elif c == ')':
            current_position.update(current_ends)
            current_starts, current_ends = stack.pop()
        elif c == '|':
            current_ends.update(current_position)
            current_position = current_starts
        else:
            assert False
    return edges

def solve_maze(edges):
    queue = [(0, 0, 0)]
    seen = set()
    max_cost = 0
    at_least_1000 = set()
    while queue:
        cost, y, x = heappop(queue)
        if (y, x) in seen:
            continue
        seen.add((y, x))
        if cost >= 1000:
            at_least_1000.add((y, x))
        if cost > max_cost:
            max_cost = cost
        for ny, nx in n(edges, y, x):
            heappush(queue, (cost+1, ny, nx))
    return max_cost, len(at_least_1000)

def solve(input_data):
    edges = parse_regex2(input_data)
    return solve_maze(edges)

print(solve("^WNE$"))
print(solve("^ENWWW(NEEE|SSE(EE|N))$"))
print(solve("^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"))
print(solve("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$"))
print(solve("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$"))
print(solve("^NNNNN(EEEEE|NNN)NNNNN$"))
print(solve(data))
