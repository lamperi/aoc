example = """In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A."""
import os.path
INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read().strip()


def func(data):
    steps = 6
    start_state = "A"
    state = None
    states = {}
    for line in data.splitlines():
        if line.startswith("Begin in state"):
            start_state = line.split()[-1][:-1]
        elif line.startswith("Perform a diagnostic checksum after"):
            steps = int(line.split()[-2])
        elif line.startswith("In state"):
            state = line.split()[-1][:-1]
            if state not in states:
                states[state] = {}
        elif line.strip().startswith("If the current value is"):
            current_value = int(line.split()[-1][:-1])
        elif line.strip().startswith("- Write the value"):
            write_value = int(line.split()[-1][:-1])
        elif line.strip().startswith("- Move one slot to the"):
            dir = line.split()[-1][:-1]
            dir = -1 if dir == "left" else 1
        elif line.strip().startswith("- Continue with state"):
            next_state = line.split()[-1][:-1]
            states[state][current_value] = (write_value, dir, next_state)

    tape = [0]*10000
    position = 5000
    current_state = start_state
    for i in range(steps):
        current_value = tape[position]
        write, dir, next = states[current_state][current_value]
        tape[position] = write
        position += dir
        current_state = next

    return sum(tape)


print("Example (3)   :", func(example))
print("Part 1        :", func(data))
