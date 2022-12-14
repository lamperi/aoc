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
        match one[i], two[i]:
            case int(a), int(b):
                if a < b:
                    return -1
                elif a > b:
                    return 1
            case list(a), list(b):
                if (r := compare(a, b)) != 0:
                    return r
            case list(a), int(b):
                if (r := compare(a, [b])) != 0:
                    return r
            case int(a), list(b):
                if (r := compare([a], b)) != 0:
                    return r
        i += 1
    if len(one) > len(two):
        return 1
    elif len(one) < len(two):
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

