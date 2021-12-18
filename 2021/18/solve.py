import os.path
from itertools import permutations
from math import ceil
from copy import deepcopy

INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

def add_left(s, index, k):
    if isinstance(s[index], int):
        s[index] += k
    else:
        while isinstance(s[index], list):
            s=s[index]
            index=-1
        s[index] += k

def add_right(s, index, k):
    if isinstance(s[index], int):
        s[index] += k
    else:
        while isinstance(s[index], list):
            s=s[index]
            index=0
        s[index] += k

def explode(number):
    for i,a in enumerate(number):
        if isinstance(a, list):
            for j,b in enumerate(a):
                if isinstance(b, list):
                    for k,c in enumerate(b):
                        if isinstance(c, list):
                            for n,d in enumerate(c):
                                if isinstance(d, list):
                                    if n > 0:
                                        add_left(c, n-1, d[0])
                                    elif k > 0:
                                        add_left(b, k-1, d[0])
                                    elif j > 0:
                                        add_left(a, j-1, d[0])
                                    elif i > 0:
                                        add_left(number, i-1, d[0])
                                    if n < len(c)-1:
                                        add_right(c, n+1, d[1])
                                    elif k < len(b)-1:
                                        add_right(b, k+1, d[1])
                                    elif j < len(a)-1:
                                        add_right(a, j+1, d[1])
                                    elif i < len(number)-1:
                                        add_right(number, i+1, d[1])
                                    c[n] = 0
                                    return number
    for i,a in enumerate(number):
        if isinstance(a, int) and a > 9:
            p = [a//2, int(ceil(a/2))]
            number[i] = p
            return number
        elif isinstance(a, list):
            for j,b in enumerate(a):
                if isinstance(b, int) and b > 9:
                    p = [b//2, int(ceil(b/2))]
                    a[j] = p
                    return number
                elif isinstance(b, list):
                    for k,c in enumerate(b):
                        if isinstance(c, int) and c > 9:
                            p = [c//2, int(ceil(c/2))]
                            b[k] = p
                            return number
                        elif isinstance(c, list):
                            for n,d in enumerate(c):
                                if isinstance(d, int) and d > 9:
                                    p = [d//2, int(ceil(d/2))]
                                    c[n] = p
                                    return number
    return None

def magnitude(n):
    if isinstance(n, list):
        assert len(n)==2
        return 3*magnitude(n[0])+2*magnitude(n[1])
    elif isinstance(n, int):
        return n

def fully_reduce(number):
    while explode(number):
        pass
    return number

def part1(data,no_mag=False):
    snail=[]
    for line in data.splitlines():
        snail.append(eval(line))
    total=snail[0]
    for number in snail[1:]:
        total = fully_reduce([total] + [number])
    if no_mag:
        return total
    return magnitude(total)

assert([[[[0,9],2],3],4]==explode([[[[[9,8],1],2],3],4]))
assert([7,[6,[5,[7,0]]]]==explode([7,[6,[5,[4,[3,2]]]]]))
assert([[6,[5,[7,0]]],3]==explode([[6,[5,[4,[3,2]]]],1]))
assert([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]==explode([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]))
assert([[[[0,7],4],[[7,8],[0,13]]],[1,1]]==explode([[[[0,7],4],[15,[0,13]]],[1,1]]))
assert(143==magnitude([[1,2],[[3,4],5]]))
assert(3488==magnitude([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]))
assert([[[[1,1],[2,2]],[3,3]],[4,4]]==part1("""[1,1]
[2,2]
[3,3]
[4,4]""",no_mag=True))
assert([[[[3,0],[5,3]],[4,4]],[5,5]]==part1("""[1,1]
[2,2]
[3,3]
[4,4]
[5,5]""",no_mag=True))
assert([[[[5,0],[7,4]],[5,5]],[6,6]]==part1("""[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]""",no_mag=True))
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

def part2(data):
    snail=[]
    for line in data.splitlines():
        snail.append(eval(line))
    return max(
        magnitude(fully_reduce([deepcopy(a)]+[deepcopy(b)]))
        for a,b in permutations(snail, 2) 
    )

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

