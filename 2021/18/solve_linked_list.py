from __future__ import annotations
import os.path
from itertools import permutations, pairwise
from functools import reduce
from dataclasses import dataclass

INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

@dataclass
class Node:
    token: int|str
    next: Node = None

class LinkedList:
    head: Node = None
    def __init__(self, iterable):
        prev = None
        for prev_token,token in pairwise(iterable):
            if prev is None:
                self.head = Node(token=prev_token)
                prev = self.head
            v = Node(token=token)
            prev.next = v
            prev = v
    
    def __iter__(self):
        curr = self.head
        while curr:
            yield curr.token
            curr = curr.next
    
    def __eq__(self, other):
        return self.head == other.head
    
    def nodes(self):
        curr = self.head
        while curr:
            yield curr
            curr = curr.next

def explode(number):
    nesting = 0
    prev_number_node = None
    start_range = None
    for node in number.nodes():
        token = node.token
        if token == "[":
            nesting += 1
            if nesting < 5:
                continue
            clear_range = node
            # explode inline
            node = node.next  # first number
            if prev_number_node is not None:
                prev_number_node.token += node.token
            node = node.next.next  # , and second number
            set_num = node.token
            node = node.next.next  # end brace and next token
            clear_range.token = 0
            clear_range.next = node
            # find next int node
            while node and not isinstance(node.token, int):
                node = node.next
            if node is not None:
                node.token += set_num
            return number
        elif token == "]":
            nesting -= 1
        elif isinstance(token, int):
            prev_number_node = node

def split(number):
    for node in number.nodes():
        token = node.token
        if isinstance(token, int) and token > 9:
            n = node.next
            node.token = "["
            for t in (token//2, ",", (token+1)//2, "]"):
                no = Node(token=t)
                node.next = no
                node = no
            node.next = n
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
    number = LinkedList(number)
    while explode(number) or split(number):
        pass
    return list(number)

def tokenize(line):
    tokens=[]
    n=""
    for c in line:
        if c in "[],":
            if n:
                tokens.append(int(n))
                n=""
            tokens.append(c)
        else:
            n+=c
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

assert(LinkedList(tokenize("[[[[0,9],2],3],4]"))==explode(LinkedList(tokenize("[[[[[9,8],1],2],3],4]"))))
assert(LinkedList(tokenize("[7,[6,[5,[7,0]]]]"))==explode(LinkedList(tokenize("[7,[6,[5,[4,[3,2]]]]]"))))
assert(LinkedList(tokenize("[[6,[5,[7,0]]],3]"))==explode(LinkedList(tokenize("[[6,[5,[4,[3,2]]]],1]"))))
assert(LinkedList(tokenize("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"))==explode(LinkedList(tokenize("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]"))))
assert(LinkedList(tokenize("[[[[0,7],4],[[7,8],[0,13]]],[1,1]]"))==split(LinkedList(tokenize("[[[[0,7],4],[15,[0,13]]],[1,1]]"))))
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
