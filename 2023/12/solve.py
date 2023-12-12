import os.path
import itertools
import collections

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

### Orig Part 1. Slow implementation with all combinations.

def count_damaged_groups(springs):
    return [len(g) for g in springs.split(".") if g]

def valid(springs, damaged_spring_counts):
    return count_damaged_groups(springs) == damaged_spring_counts

def solve_one(springs, damaged_spring_counts):
    unknown_index = [i for i, c in enumerate(springs) if c == "?"]
    current_damaged_count = sum(1 for c in springs if c == "#")
    total_damaged_count = sum(damaged_spring_counts)
    unknown_damaged = total_damaged_count - current_damaged_count
    
    s = 0
    for damaged in itertools.combinations(unknown_index, unknown_damaged):
        solved_springs = []
        for i, c in enumerate(springs):
            if c != "?":
                solved_springs.append(c)
            elif i in damaged:
                solved_springs.append("#")
            else:
                solved_springs.append(".")
        if valid("".join(solved_springs), damaged_spring_counts):
            s += 1
    return s

def part1(data):
    s = 0
    for line in data.splitlines():
        springs, damaged_spring_counts = line.split()
        damaged_spring_counts = [int(x) for x in damaged_spring_counts.split(",")]
        s += solve_one(springs, damaged_spring_counts)
    return s

test = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""
if False: # Very slow
    print(part1(test))
    print(part1(data))

### Part 2. Implemented with dynamic programming, also solves part 1. Much quicker.

def solve_one_part2(springs, damaged_spring_counts):
    # state: (number_of_damaged_behind, number_of_clues_processed)
    init_state = (0, 0)
    states = {init_state: 1}
    springs += "." # Handle end case nicely.
    for c in springs:
        new_states = collections.defaultdict(int)
        for ((current_damage, clues_processed), combinations) in states.items():
            match c:
                case '#':
                    if clues_processed < len(damaged_spring_counts) and current_damage < damaged_spring_counts[clues_processed]:
                        new_state = (current_damage+1, clues_processed)
                        new_states[new_state] += combinations
                case ".":
                    if current_damage == 0:
                        new_state = (0, clues_processed)
                        new_states[new_state] += combinations
                    elif current_damage == damaged_spring_counts[clues_processed]:
                        new_state = (0, clues_processed+1)
                        new_states[new_state] += combinations
                case "?":
                    if clues_processed < len(damaged_spring_counts) and current_damage < damaged_spring_counts[clues_processed]:
                        new_state = (current_damage+1, clues_processed)
                        new_states[new_state] += combinations
                    if current_damage == 0:
                        new_state = (0, clues_processed)
                        new_states[new_state] += combinations
                    elif current_damage == damaged_spring_counts[clues_processed]:
                        new_state = (0, clues_processed+1)
                        new_states[new_state] += combinations
                case a:
                    assert False, f"got {a}??"
        states = new_states
    s = 0
    for ((current_damage, clues_processed), combinations) in states.items():
        if current_damage == 0 and clues_processed == len(damaged_spring_counts):
            s += combinations
    return s
    
def part2(data, fac=5):
    s = 0
    for line in data.splitlines():
        springs, damaged_spring_counts = line.split()
        damaged_spring_counts = [int(x) for x in damaged_spring_counts.split(",")]
        springs = "?".join([springs] * fac)
        damaged_spring_counts = damaged_spring_counts * fac
        s += solve_one_part2(springs, damaged_spring_counts)
    return s

# part 1 again!
print(part2(test, fac=1))
print(part2(data, fac=1))

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))
