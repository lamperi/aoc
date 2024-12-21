import os.path
from collections import deque
from functools import cache

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def as_map(pad):
    return {
        button: (y, x)
        for y, row in enumerate(pad)
        for x, button in enumerate(row)
        if button != ' '
    }

NUMBER_POS = as_map((
    ('7', '8', '9'),
    ('4', '5', '6'),
    ('1', '2', '3'),
    (' ', '0', 'A')
))
ARROW_POS = as_map((
    (' ', '^', 'A'),
    ('<', 'v', '>')
))

MOVES = {
    '^': (-1, 0),
    '<': (0, -1),
    'v': (1, 0),
    '>': (0, 1),
}

class Robot():
    def __init__(self, kb, state='A', store=None):
        self.kb = kb
        self.state = state
        self.store = store
    
    def apply(self, button):
        if self.store is not None:
            self.store.append(button)
        if button in MOVES:
            pos = self.kb[self.state]
            move = MOVES[button]
            next_pos = pos[0] + move[0], pos[1] + move[1]
            next_state = [ch for ch,pos in self.kb.items() if pos == next_pos]
            if len(next_state) == 1:
                self.state = next_state[0]
                return None, True
            else:
                return None, False
        else:
            return self.state, True

    def copy(self):
        return Robot(self.kb, self.state, store=self.store[:] if self.store is not None else None)

def get_number_paths(start, end):
    y0, x0 = NUMBER_POS[start]
    y1, x1 = NUMBER_POS[end]
    yd = y1-y0
    xd = x1-x0
    ys = '>' if yd > 0 else '<'
    xd = '^' if xd < 0 else 'v'
    if yd != 0 and xd != 0:
        return [
            (ys * yd) + (xd * xd) + 'A',
            (xd * xd) + (ys * yd) + 'A'
        ]
    # if one or two dimensions are 0 just return one path.
    return [
        (ys * yd) + (xd * xd) + 'A',
    ]

# This doesn't scale.
def solve(code):
    robots = [Robot(NUMBER_POS)]
    for i in range(2):
        robots.append(Robot(ARROW_POS))
    state = ('', robots, [])

    queue = deque([state])
    visited = set()
    vs = ('',) + tuple(r.state for r in robots)
    visited.add(vs)
    while queue:
        prefix, robots0, store0 = queue.popleft()
        for button in '^<v>A':
            robots = [r.copy() for r in robots0]
            store = store0[:]
            store.append(button)
            
            wrote = None
            for robot in reversed(robots):
                button, valid = robot.apply(button)
                if not valid or button is None:
                    break
            else:
                wrote = button
            if wrote is None:
                st = (prefix,) + tuple(r.state for r in robots)
                if st in visited:
                    continue
                visited.add(st)
                queue.append((prefix, robots, store))
            else:
                new_prefix = prefix + wrote
                if new_prefix == code:
                    return store
                if code.startswith(new_prefix):
                    st = (new_prefix,) + tuple(r.state for r in robots)
                    if st in visited:
                        continue
                    visited.add(st)
                    queue.append((new_prefix, robots, store))


def part1(data):
    codes = data.splitlines()
    ans = 0
    for code in codes:
        seq = solve(code)
        ans += len(seq) * int(code[:-1])
    return ans


# This is cacheable but by caching solve_robots
# this is effectively cached too.
#@cache
def shortest_path(start, end, is_numpad):
    # This method solves the shortest paths
    # which may make sense. Only paths
    # which change the pressed button the least
    # times are considered. It actually doesn't make
    # much different with the correct caching on 
    # solve robots
    if is_numpad:
        graph = NUMBER_POS
    else:
        graph = ARROW_POS
    valid_pos = set(graph.values())
    start_pos = graph[start]
    end_pos = graph[end]
    q = deque([(start_pos, '')])
    paths = []
    while q:
        pos, path = q.popleft()
        if pos == end_pos:
            paths.append(path + 'A')
            continue
        if paths and len(paths[0]) < len(path) + 1:
            continue
        for code in '^v<>':
            dir = MOVES[code]
            next_pos = pos[0] + dir[0], pos[1] + dir[1]
            if next_pos in valid_pos:
                q.append((next_pos, path + code))
    # How many times button changes during the sequence?
    # This is a heuristic but works.
    min_entropy = 10
    for p in paths:
        entropy = 0
        for a, b in zip(p, p[1:]):
            if a != b:
                entropy += 1
        min_entropy = min(entropy, min_entropy)
    ret = []
    for p in paths:
        entropy = 0
        for a, b in zip(p, p[1:]):
            if a != b:
                entropy += 1
        if entropy == min_entropy:
            ret.append(p)
    return ret

@cache
def solve_robots(code, arrow_robot_count, is_numpad):
    # This the the human operator.
    if arrow_robot_count == 0:
        return len(code)
    state = 'A'
    min_path = 0
    for point in code:
        shortest_paths = shortest_path(state, point, is_numpad)
        min_path += min(
            solve_robots(path, arrow_robot_count-1, is_numpad=False)
            for path in shortest_paths
        )
        state = point
    return min_path

def part2(data, keypad_robots=25):
    codes = data.splitlines()
    ans = 0
    for code in codes:
        seq_len = solve_robots(code, keypad_robots + 1, is_numpad=True)
        ans += seq_len * int(code[:-1])
    return ans

test = """029A
980A
179A
456A
379A"""
assert 126384 == part1(test)
print(part1(data))

# Override test for part 2.
# test = """ """

assert 126384 == part2(test, keypad_robots=2)
print(part2(data))
#print(solve_robots.cache_info())