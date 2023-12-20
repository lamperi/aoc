import os.path
import math
import itertools

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def parse_and_init_modules(data):
    modules = {}
    for line in data.splitlines():
        module, targets = line.split(" -> ")
        targets = targets.split(", ")
        if module[0] in "%&":
            module_type = module[0]
            module = module[1:]
        else:
            module_type = "broadcaster"
        modules[module] = {"type": module_type, "targets": targets}
    
    for module, info in modules.items():
        if info["type"] == "&":
            mem = {}
            for m, i in modules.items():
                if module in i["targets"]:
                    mem[m] = "low"
            info["memory"] = mem
        if info["type"] == "%":
            info["state"] = False

    return modules

def do_the_loop(modules, button_presses, callback):
    for button_press in button_presses:
        state = [("broadcaster", "low", "push")]
        while state:
            module, pulse, source = state.pop(0)
            if v := callback(button_press, module, pulse):
                return v
            if module not in modules:
                # output
                continue
            info = modules[module]
            module_type, targets = info["type"], info["targets"]
            match module_type:
                case "broadcaster":
                    for t in targets:
                        state.append((t, pulse, module))
                case "&":
                    memory = info["memory"]
                    memory[source] = pulse
                    if all(v == "high" for v in memory.values()):
                        pulse = "low"
                    else:
                        pulse = "high"
                    for t in targets:
                        state.append((t, pulse, module))
                case "%":
                    if pulse == "high":
                        continue
                    info["state"] = not info["state"]
                    if info["state"]:
                        pulse = "high"
                    else:
                        pulse = "low"
                    for t in targets:
                        state.append((t, pulse, module))

def part1(data):
    modules = parse_and_init_modules(data)
    low_pulses = 0
    high_pulses = 0
    def hijack_arrived(_button_press, _module, pulse):
        nonlocal low_pulses
        nonlocal high_pulses
        if pulse == "low":
            low_pulses += 1
        elif pulse == "high":
            high_pulses += 1
    do_the_loop(modules, range(1000), hijack_arrived)
    return low_pulses * high_pulses

test = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""
print(part1(test))
print(part1(data))

def part2(data):
    modules = parse_and_init_modules(data)
    # My input looks like:
    # 
    # &fn  &fh   &lk  &hh <--- All low
    #  |    |     |    |
    #  \    \     /    /
    #   \---- &nc ----/  <-- becomes all high!
    #          |
    #         rx <-- get low pulse, profit.
    # 
    # The expectation is to find when do
    # fn, fh, lk and hh get low pulse.
    # if in cycles, multiplying them should
    # be the answer here.
    
    sources = {}
    for module, info in modules.items():
        for t in info["targets"]:
            if t not in sources:
                sources[t] = []
            sources[t].append(module)

    important_nodes = []
    for n in sources["rx"]:
        important_nodes.extend(sources[n])
    important_last_low = {n: 0 for n in important_nodes}
    important_cycle = {n: [] for n in important_nodes}

    def hijack_arrived(button_press, module, pulse):
        if pulse == "low" and module in important_nodes:
            p = important_last_low[module]
            important_last_low[module] = button_press
            important_cycle[module].append(button_press - p)
            if all(cycle for cycle in important_cycle.values()):
                return math.prod(cycle[0] for cycle in important_cycle.values())

    return do_the_loop(modules, itertools.count(start=1), hijack_arrived)

# Override test for part 2.
# test = """ """

print(part2(data))