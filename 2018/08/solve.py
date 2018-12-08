data = open("input.txt").read().strip()

import re
import string
from collections import Counter

example = """2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"""


class Node:

    def __init__(self):
        self.child = []
        self.metadata = []

    def count_metadata(self):
        return sum(c.count_metadata() for c in self.child) + sum(self.metadata)

    def count_value(self):
        if self.child:
            return sum(self.child[m-1].count_value() for m in self.metadata if 0 < m <= len(self.child))
        else:
            return sum(self.metadata)

def build_tree(nodes, index):
    child_count = nodes[index]
    metadata_count = nodes[index+1]
    index += 2

    node = Node()
    for _ in range(child_count):
        child, index = build_tree(nodes, index)
        node.child.append(child)
    for _ in range(metadata_count):
        node.metadata.append(nodes[index])
        index += 1
    return node, index

def solve1(data):
    nodes = list(map(int, data.split()))
    root, _ = build_tree(nodes, 0)
    return root.count_metadata()

print(solve1(example))
print(solve1(data))

def solve2(data):
    nodes = list(map(int, data.split()))
    root, _ = build_tree(nodes, 0)
    return root.count_value()

print(solve2(example))
print(solve2(data))
