import os.path
from collections import deque
import time

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()
INPUT = os.path.join(os.path.dirname(__file__), 'test_input.txt')
with open(INPUT) as f:
    test = f.read()

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

print(part1(test))
print(part1(data))

def solve_recursively(buttons_that_increment_state, buttons, state, target_state, pressed_buttons, presses=0):
    if state == target_state:
        return presses

    min_len = 100
    min_idx = None
    min_buttons = None

    for j, inc in enumerate(buttons_that_increment_state):
        valid_buttons = set(inc) - pressed_buttons
        if len(valid_buttons) < min_len and valid_buttons:
            min_len = len(valid_buttons)
            min_buttons = valid_buttons
            min_idx = j
    if min_buttons is None:
        return None

    newly_pressed_buttons = pressed_buttons | min_buttons
    min_buttons = list(min_buttons)
    
    needed_presses = target_state[min_idx] - state[min_idx]
    best_path = None
    for comb in get_sum_combinations(min_len, needed_presses):
        new_state = state[:]
        for a, aa in zip(min_buttons, comb):
            for i in buttons[a]:
                new_state[i] += aa
        if reachable(new_state, target_state):
            r = solve_recursively(buttons_that_increment_state, buttons, new_state, target_state, newly_pressed_buttons, presses + needed_presses)
            if r is not None:
                if best_path is None:
                    best_path = r
                else:
                    best_path = min(best_path, r)
    return best_path

def get_sum_combinations(component_count, total_sum):
    if component_count > 1:
        for n in range(0, total_sum + 1):
            for t in get_sum_combinations(component_count - 1, total_sum - n):
                yield (n,) + t
    else:
        yield (total_sum,)

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
        #print(f"Solving problem {i+1}/{len(problems)}")
        target_state = problem[0]
        schematics = problem[1]

        buttons_that_increment_state = [[] for _ in target_state]
        for i, buttons in enumerate(schematics):
            for b in buttons:
                buttons_that_increment_state[b].append(i)

        start_time = time.time()
        state = [0 for _ in target_state]
        ret = solve_recursively(buttons_that_increment_state, schematics, state, list(target_state), set())
        end_time = time.time()
        taken = f'{end_time-start_time:.3f}'
        #print(f"found by solver: {ret} in {taken} seconds")
        assert ret is not None
        total_presses += ret
                    
    return total_presses

def reachable(state, target_state):
    for a, b in zip(state, target_state):
        if a > b:
            return False
    return True

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))