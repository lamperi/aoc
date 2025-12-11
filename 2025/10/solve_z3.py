import os.path
import z3

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()
INPUT = os.path.join(os.path.dirname(__file__), 'test_input.txt')
with open(INPUT) as f:
    test = f.read()

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
    for j, problem in enumerate(problems):
        target_state = problem[0]
        buttons = problem[1]
        
        button_press_symbol_names = [f"press_{i}" for i in range(len(buttons))]
        button_symbols = z3.Ints(button_press_symbol_names)
        s = z3.Optimize()
        for symbol in button_symbols:
            s.add(symbol >= 0)
        joltage_equations = [None for _ in target_state]
        for i, counters in enumerate(buttons):
            for _, butt in enumerate(counters):
                if joltage_equations[butt] is None:
                    joltage_equations[butt] = button_symbols[i]
                else:
                    joltage_equations[butt] += button_symbols[i]
        for i, state in enumerate(target_state):
            joltage_equations[i] = joltage_equations[i] == state
        for e in joltage_equations:
            s.add(e)
        total_presses_eq = button_symbols[0]
        for symbol in button_symbols[1:]:
            total_presses_eq += symbol
        s.minimize(total_presses_eq)
        s.check()
        m = s.model()
        solution = m.evaluate(total_presses_eq).as_long()
        #print(f"Solving problem {j+1}/{len(problems)}, got {solution}")
        total_presses += solution

    return total_presses

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))