import os.path
import functools 

FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(FILE) as f:
    INPUT = f.read()

TEST = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""

def compare(one, two):
    i = 0

    while i < len(one) and i < len(two):
        if isinstance(one[i], int) and isinstance(two[i], int):
            if two[i] > one[i]:
                return -1
            elif two[i] < one[i]:
                return 1
        elif isinstance(one[i], list) and isinstance(two[i], list):
            if (r := compare(one[i], two[i])) != 0:
                return r
        elif isinstance(one[i], list):
            first = one[i]
            second = [two[i]]
            if (r := compare(first, second)) != 0:
                return r
        else:
            first = [one[i]]
            second = two[i]
            if (r := compare(first, second)) != 0:
                return r
        i += 1
    if len(two) < len(one):
        return 1
    elif len(two) > len(one):
        return -1
    return 0

def solve(data):
    packets = data.split("\n\n")
    s = 0
    for packet_index, packet in enumerate(packets, start=1):
        one, two = packet.strip().split("\n")
        one = eval(one)
        two = eval(two)

        if compare(one, two) == -1:
            s += packet_index
    return s
        
def solve2(data):
    packets = [eval(p) for p in data.split() if p.strip()]
    packets.append([[2]])
    packets.append([[6]])
    packets = sorted(packets, key=functools.cmp_to_key(compare))
    a = packets.index([[2]]) + 1
    b = packets.index([[6]]) + 1
    return a*b

print(solve(TEST))
print(solve(INPUT))

print(solve2(TEST))
print(solve2(INPUT))

