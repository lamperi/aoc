import os.path
from itertools import permutations
from functools import reduce
from copy import deepcopy

INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

def add_to_list(s, k, init_index, second_index):
    index=init_index
    while isinstance(s[index], list):
        s=s[index]
        index=second_index
    s[index] += k

def explode(number, parent_indexes=(), parent_nodes=()):
    parent_nodes+=(number,)
    for i,a in enumerate(number):
        if not isinstance(a, list):
            continue
        added = [False, False]
        if len(parent_nodes) == 4:
            number[i] = 0
            for j, b in zip(reversed(parent_indexes + (i,)), reversed(parent_nodes)):
                k = 1-j
                if added[j]:
                    continue
                add_to_list(b, a[k], k, j)
                added[j] = True
            return number
        elif explode(a, parent_indexes + (i,), parent_nodes):
            return number

def split(number):
    for i, a in enumerate(number):
        if not isinstance(a, list) and a > 9:
            number[i] = [a//2, (a+1)//2]
            return number
        elif isinstance(a, list):
            if split(a):
                return number
        
def magnitude(n):
    if isinstance(n, list):
        return 3*magnitude(n[0])+2*magnitude(n[1])
    return n

def fully_reduce(number):
    while explode(number) or split(number):
        pass
    return number

def parse(data):
    return (eval(line) for line in data.splitlines())

def part1(data):
    return magnitude(reduce(lambda n1, n2: fully_reduce([n1, n2]), parse(data)))

def part2(data):
    return max(
        magnitude(fully_reduce(deepcopy([a,b])))
        for a,b in permutations(parse(data), 2) 
    )

assert([[[[0,9],2],3],4]==explode([[[[[9,8],1],2],3],4]))
assert([7,[6,[5,[7,0]]]]==explode([7,[6,[5,[4,[3,2]]]]]))
assert([[6,[5,[7,0]]],3]==explode([[6,[5,[4,[3,2]]]],1]))
assert([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]==explode([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]))
assert([[[[0,7],4],[[7,8],[0,13]]],[1,1]]==split([[[[0,7],4],[15,[0,13]]],[1,1]]))
assert(143==magnitude([[1,2],[[3,4],5]]))
assert(3488==magnitude([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]))
assert(4140 == part1("""[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""))
print(part1(data), "[PART 1]")

assert(3993 == part2("""[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""))

print(part2(data), "[PART 2]")
