import os.path
from itertools import permutations
from functools import reduce

INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

def explode(number):
    nesting = 0
    prev_number_index = None
    state = 0
    for index, token in enumerate(number):
        if token == "[":
            nesting += 1
            if nesting == 5 and state == 0:
                #print("before")
                #print(number, index)
                assert isinstance(number[index+1], int)
                assert isinstance(number[index+3], int)
                if prev_number_index is not None:
                    number[prev_number_index] += number[index+1]
                state = 1
                set_num = number[index+3]
                remove_slice = slice(index,index+5)
        elif token == "]":
            nesting -= 1
        elif isinstance(token, int):
            if state == 0:
                prev_number_index = index
            elif state in (1,2):
                state += 1
            elif state == 3:
                number[index] += set_num
                state = 4
                del number[remove_slice]
                number.insert(remove_slice.start, 0)
                #print("after")
                #print(number, index)
                return number
        elif token == ",":
            pass
        else:
            print(index, token)
            assert False
    if state == 3:
        del number[remove_slice]
        number.insert(remove_slice.start, 0)
        return number

def split(number):
    for index, token in enumerate(number):
        if isinstance(token, int) and token > 9:
            del number[index]
            for j, t in enumerate(("[", token//2, ",", (token+1)//2, "]")):
                number.insert(index+j, t)
            return number
    return
        
def magnitude(n):
    m = 0
    f = 1
    for token in n:
        if isinstance(token, int):
            m += token*f
        elif token == "[":
            f *= 3
        elif token == "]":
            f = f//2
        elif token == ",":
            f = f//3 * 2
    return m

def fully_reduce(number):
    while explode(number) or split(number):
        pass
    return number

def tokenize(line):
    tokens=[]
    n=[]
    for c in line:
        if c in "[],":
            if n:
                tokens.append(int("".join(n)))
                n=[]
            tokens.append(c)
        else:
            n.append(c)
    return tokens

def combine_tokens(tokens1, tokens2):
    return ["["] + tokens1 + [","] + tokens2 + ["]"]

def parse(data):
    return (tokenize(line) for line in data.splitlines())

def part1(data):
    return magnitude(reduce(lambda n1, n2: fully_reduce(combine_tokens(n1, n2)), parse(data)))

def part2(data):
    return max(
        magnitude(fully_reduce(combine_tokens(a,b)))
        for a,b in permutations(parse(data), 2) 
    )

assert(tokenize("[[[[0,9],2],3],4]")==explode(tokenize("[[[[[9,8],1],2],3],4]")))
assert(tokenize("[7,[6,[5,[7,0]]]]")==explode(tokenize("[7,[6,[5,[4,[3,2]]]]]")))
assert(tokenize("[[6,[5,[7,0]]],3]")==explode(tokenize("[[6,[5,[4,[3,2]]]],1]")))
assert(tokenize("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")==explode(tokenize("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]")))
assert(tokenize("[[[[0,7],4],[[7,8],[0,13]]],[1,1]]")==split(tokenize("[[[[0,7],4],[15,[0,13]]],[1,1]]")))
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
