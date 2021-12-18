from __future__ import annotations
import os.path
from itertools import permutations, pairwise
from functools import reduce
from dataclasses import dataclass

INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

def explode(number):
    for i, (n, d) in enumerate(number):
        if d == 5:
            if i > 0:
                number[i-1][0] += n
            if i < len(number)-2:
                number[i+2][0] += number[i+1][0]
            number[i][0] = 0
            number[i][1] -= 1
            del number[i+1]
            return number

def split(number):
    for i, (n, d) in enumerate(number):
        if n > 9:
            number[i] = [(n+1)//2, d+1]
            number.insert(i, [n//2, d+1])
            return number
        
def magnitude(num):
    num = num[:]
    while len(num) > 1:
        for i, ((n, d), (nn, dd)) in enumerate(pairwise(num)):
            if d == dd:
                num[i] = [3*n+2*nn, d-1]
                del num[i+1]
                break
    assert num[0][1] == 0
    return num[0][0]

def fully_reduce(number):
    while explode(number) or split(number):
        pass
    return number

def combine_tokens(tokens1, tokens2):
    return [[n, d+1] for n, d in tokens1] + [[n, d+1] for n, d in tokens2]

def tokenize(line):
    tokens=[]
    n=""
    depth=0
    for c in line:
        if c in "[],":
            if n:
                tokens.append([int(n), depth])
                n=""
            if c == "[":
                depth += 1
            elif c == "]":
                depth -= 1
        else:
            n+=c
    return tokens

def parse(data):
    return (tokenize(line) for line in data.splitlines())

def part1(data):
    return magnitude(reduce(lambda n1, n2: fully_reduce(combine_tokens(n1, n2)), parse(data)))

def part2(data):
    return max(
        magnitude(fully_reduce(combine_tokens(a,b)))
        for a,b in permutations(parse(data), 2) 
    )

assert((tokenize("[[[[0,9],2],3],4]"))==explode((tokenize("[[[[[9,8],1],2],3],4]"))))
assert((tokenize("[7,[6,[5,[7,0]]]]"))==explode((tokenize("[7,[6,[5,[4,[3,2]]]]]"))))
assert((tokenize("[[6,[5,[7,0]]],3]"))==explode((tokenize("[[6,[5,[4,[3,2]]]],1]"))))
assert((tokenize("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"))==explode((tokenize("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]"))))
assert((tokenize("[[[[0,7],4],[[7,8],[0,13]]],[1,1]]"))==split((tokenize("[[[[0,7],4],[15,[0,13]]],[1,1]]"))))
assert(143==magnitude(tokenize("[[1,2],[[3,4],5]]")))
assert(3488==magnitude(tokenize("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")))
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
