example = """#..#.#..##......###...###""", """...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
"""

data = """.##..##..####..#.#.#.###....#...#..#.#.#..#...#....##.#.#.#.#.#..######.##....##.###....##..#.####.#""", """.#... => #
#.... => .
#.### => .
#.##. => .
#...# => .
...#. => .
.#..# => #
.#### => #
.###. => .
###.. => #
##### => .
....# => .
.#.## => #
####. => .
##.#. => #
#.#.# => #
..#.# => .
.#.#. => #
###.# => #
##.## => .
..#.. => .
..... => .
..### => #
#..## => #
##... => #
...## => #
##..# => .
.##.. => #
#..#. => .
#.#.. => #
.##.# => .
..##. => ."""

def solve(state, rules, gens):
    rules = [rule.split(" => ") for rule in rules.splitlines() if rule.split(" => ")[1] == '#']

    BUF = gens*2
    state = ['.'] * BUF + list(state) + ['.'] * BUF
    for g in range(gens):
        next_state = state[:]
        for index in range(len(state)-5):
            for rule, pot_state in rules:
                cur = ''.join(state[index:index+5])
                if cur == rule:
                    next_state[index+2] = pot_state
                    break
            else:
                next_state[index+2] = '.'
        state = next_state
    s = 0
    for i, c in enumerate(state):
        if c == '#':
            s += i - BUF
    return s

print(solve(example[0], example[1], 20))
print(solve(data[0], data[1], 20))


def solve2(state, rules, i_prev, i_next):
    s_prev = solve(state, rules, i_prev)
    s_next = solve(state, rules, i_next)
    return (50000000000 - i_next)*(s_next - s_prev) + s_next

# Part 2: observed that number grows linearly after a certain time
print(solve2(data[0], data[1], 299, 300))
# Just to double check with another range
print(solve2(data[0], data[1], 240, 241))