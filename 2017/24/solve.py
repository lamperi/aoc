example = """0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10"""
data = open("input.txt").read()

from collections import defaultdict


def search(current, components, strength, bridge, by_length=True):
    if by_length:
        strengths = [(len(bridge), strength)]
    else:
        strengths = [strength]
    for choice in components[current]:
        copy_dict = components.copy()

        set_copy = components[current].copy()
        set_copy.remove(choice)
        copy_dict[current] = set_copy

        set_copy = components[choice].copy()
        set_copy.remove(current)
        copy_dict[choice] = set_copy

        bridge_copy = bridge.copy()
        bridge_copy.append((current, choice))
        max_strength = search(choice, copy_dict, strength + current + choice, bridge_copy, by_length)
        if by_length:
            strengths.append(max_strength)
        else:
            strengths.append(max_strength)

    return max(strengths)


def func(data, by_length):
    components = defaultdict(lambda: set())
    for line in data.splitlines():
        p = line.split("/")
        components[int(p[0])].add(int(p[1]))
        components[int(p[1])].add(int(p[0]))

    return search(0, components, 0, [], by_length)


print("Example (1)   :", func(example, False))
print("Part 1        :", func(data, False))
print("Example (2)   :", func(example, True))
print("Part 2        :", func(data, True))
