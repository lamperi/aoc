import os.path
from collections import deque
import heapq
import sympy

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def part1(data):
    problems = []
    for line in data.splitlines():
        parts = line.split()
        target = parts[0].strip("[]")
        buttons = parts[1:-1]
        button_schematics = []
        for button in buttons:
            button = tuple([int(a) for a in button.strip("()").split(",")])
            button_schematics.append(button)
        problems.append((target, button_schematics))
    
    total_presses = 0
    for problem in problems:
        start_state = problem[0].replace("#", ".")
        target_state = problem[0]
        schematics = problem[1]
        visited = set([start_state])
        queue = deque([(start_state, 0)])
        ok = False
        while queue:
            s, presses = queue.popleft()
            if s == target_state:
                total_presses += presses
                ok = True
                queue.clear()
                break
            for n in get_connected(s, schematics):
                if n not in visited:
                    visited.add(n)
                    queue.append((n, presses+1))
        assert ok
    return total_presses

def get_connected(state, schematics):
    for s in schematics:
        state_mut = list(state)
        for b in s:
            state_mut[b] = "#" if state_mut[b] == "." else "."
        yield "".join(state_mut)

test = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""
print(part1(test))
print(part1(data))

def solve_recursively(buttons_that_increment_state, buttons, target_state):
    min_len = 100
    min_idx = None
    state = [0 for _ in target_state]
    print(buttons_that_increment_state)
    for j, inc in enumerate(buttons_that_increment_state):
        if len(inc) < min_len:
            min_len = len(inc)
            min_idx = j
    if min_len == 1:
        assert False # Not implemented yet
    elif min_len == 2:
        a, b = buttons_that_increment_state[min_idx]
        needed_presses = target_state[min_idx] - state[min_idx]
        print(f"Should press buttons {a} and {b} which increments {min_idx}, total {needed_presses} times")
        for aa in range(0, needed_presses+1):
            bb = needed_presses - aa
            # Press a button aa times.
            # Press b button bb times.
            print(f"Pressing A: {a} {aa} times")
            for _ in range(aa):
                for i in buttons[a]:
                    state[i] += 1
            print(f"Pressing B: {b} {bb} times")
            for _ in range(bb):
                for i in buttons[b]:
                    state[i] += 1
            if reachable(state, target_state):
                print("Now, recurse. Pick next button.")
    else:
        assert False # Not implemented yet.

def part2(data):
    problems = []
    for line in data.splitlines():
        parts = line.split()
        joltages = tuple(int(a) for a in parts[-1].strip("{}").split(","))
        buttons = parts[1:-1]
        button_schematics = []
        for button in buttons:
            button = tuple([int(a) for a in button.strip("()").split(",")])
            button_schematics.append(button)
        problems.append((joltages, button_schematics))
    
    total_presses = 0
    for i, problem in enumerate(problems):
        print(f"Solving problem {i+1}/{len(problems)}")
        target_state = problem[0]
        start_state = tuple(0 for _ in target_state)
        schematics = problem[1]
        
        if False:
            button_symbols = sympy.symbols(f"a0:{len(schematics)}")
            A = [None for _ in target_state]
            for i, buttons in enumerate(schematics):
                for _, butt in enumerate(buttons):
                    if A[butt] is None:
                        A[butt] = button_symbols[i]
                    else:
                        A[butt] = A[butt] + button_symbols[i]
            for i, s in enumerate(target_state):
                A[i] -= s
            b = button_symbols
            print(A, b)
            res = sympy.solve(A, b)
            print(res)
            eq = 0
            for b in button_symbols:
                if b in res:
                    eq += res[b]
                else:
                    eq += b
            print(eq, type(eq))
        
        m = [[] for _ in target_state]
        for i, buttons in enumerate(schematics):
            for b in buttons:
                m[b].append(i)
        solve_recursively(m, schematics, target_state)
        print(m)
        
        if False:
            A = np.zeros((len(target_state), len(schematics)))
            b = np.array(target_state)
            for i, buttons in enumerate(schematics):
                for butt in buttons:
                    A[butt, i] = 1
            x = np.linalg.solve(A, b)
            print(x)
                
        if False:
            visited = set([start_state])
            queue = [(steps_needed(start_state, target_state), start_state, 0)]
            ok = False
            while queue:
                _, s, presses = heapq.heappop(queue)
                print(s, presses)
                if s == target_state:
                    total_presses += presses
                    ok = True
                    queue.clear()
                    break
                for n in get_joltage_connected(s, schematics):
                    if n not in visited:
                        visited.add(n)
                        if reachable(n, target_state):
                            elem = (steps_needed(n, target_state), n, presses+1)
                            heapq.heappush(queue, elem)
            assert ok
    return total_presses

def reachable(state, target_state):
    for a, b in zip(state, target_state):
        if a > b:
            return False
    return True

def steps_needed(state, target_state):
    s = 0
    for a, b in zip(state, target_state):
        s += b - a
    return s

def get_joltage_connected(state, schematics):
    for s in schematics:
        state_mut = list(state)
        for b in s:
            state_mut[b] += 1
        yield tuple(state_mut)


# Override test for part 2.
# test = """ """

print(part2(test))
#print(part2(data))