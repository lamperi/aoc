import os.path
import collections
import re
import math
import time
import itertools
from timeit import default_timer as timer
INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()


class SingleLinkedList(object):
    class Node(object):
        def __init__(self, value, next=None):
            self.value = value
            self.next = next
    
        def __repr__(self):
            return f"Node(value={self.value}, next={self.next.value})"

    @staticmethod
    def from_iterable(iterable):
        it=iter(iterable)
        cur = head = SingleLinkedList.Node(next(it))
        for v in it:
            node = SingleLinkedList.Node(v)
            cur.next, cur  = node, node
        cur.next = head
        return SingleLinkedList(head)

    def __init__(self, head):
        self.head = head

    def nodes(self):
        class Nodes(object):
            def __init__(self, node):
                self.node = node
            def __iter__(self):
                return NodeIterator(self.node)

        class NodeIterator(object):
            def __init__(self, node):
                self.node = node
                self.initial = node
                self.iterated_first = False
            def __next__(self):
                if not self.iterated_first:
                    self.iterated_first = True
                    return self.node
                self.node = self.node.next
                if self.node.value == self.initial.value:
                    raise StopIteration()
                return self.node
        return Nodes(self.head)

    def get_node_mapping(self):
        mapping = {}
        for node in self.nodes():
            mapping[node.value] = node
        return mapping

    def remove_next(self, count):
        assert count > 0
        new_head = node = self.head.next
        for _ in range(count):
            new_tail = node
            node = node.next
        self.head.next = node
        new_tail.next = new_head
        return new_head, new_tail

    def append_after(self, node, first_added, last_added):
        last_added.next = node.next
        node.next = first_added
    
    def advance(self):
        self.head = self.head.next

def solve(data, moves=100, padding=None):
    cups = [int(c) for c in data.strip()]
    if padding:
        cups.extend(range(max(cups)+1, padding+1))
    min_cup = min(cups)
    max_cup = max(cups)
    cups = SingleLinkedList.from_iterable(cups)
    node_mapping = cups.get_node_mapping()

    current_cup = cups.head.value
    move = 0
    while move < moves:
        move += 1
        first, last = cups.remove_next(3)
        clockwise_values = set([first.value, first.next.value, last.value])
        dest_cup = current_cup
        while True:
            dest_cup -= 1
            if dest_cup < min_cup:
                dest_cup = max_cup
            if dest_cup not in clockwise_values:
                break
        cups.append_after(node_mapping[dest_cup], first, last)
        cups.advance()
        current_cup = cups.head.value
    if padding is None:
        cups = "".join(str(i.value) for i in cups.nodes())
        return cups[cups.index("1")+1:] + cups[:cups.index("1")]
    else:
        node1 = node_mapping[1]
        nodea = node1.next
        nodeb = nodea.next
        a, b = nodea.value, nodeb.value
        return a*b


print(solve("32415"))
print(solve("389125467", moves=10))
print(solve("389125467"))
start = timer()
print(solve(data))
end = timer()
print("Part 1:", end - start)
start = timer()
print(solve(data, padding=1000000,moves=10000000))
end = timer()
print("Part 2:", end - start)