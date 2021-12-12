from io import TextIOBase
import os.path
import operator
from itertools import combinations, permutations
from functools import reduce, partial
from math import prod
from collections import Counter

INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

test="""7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""

def parse_input(data):
    nums=[]
    boards=[]
    for n, line in enumerate(data.splitlines()):
        if n == 0:
            nums=[int(s) for s in line.split(",")]
        elif line.strip() == "":
            board=[]
            boards.append(board)
        else:
            board.append([int(s) for s in line.split()])
    return nums, boards

def board_wins(board, found):
    for i in range(5):
        m = all(k in found for k in board[i])
        if m:
            return True
        m = all(board[j][i] in found for j in range(5))
        if m:
            return True
    return False

def part1(data):
    nums, boards = parse_input(data)
    found = set()
    for n in nums:
        found.add(n)
        for b in boards:
            win = board_wins(b, found)
            if win:
                unmarked = sum(k for r in b for k in r if k not in found)
                return unmarked*n

print(part1(test))
print(part1(data))

def part2(data):
    nums, boards = parse_input(data)
    found = set()
    won_boards = set()
    for n in nums:
        found.add(n)
        for bi, b in enumerate(boards):
            win = board_wins(b, found)
            if win:
                won_boards.add(bi)
                if len(won_boards) == len(boards):
                    unmarked = sum(k for r in b for k in r if k not in found)
                    return unmarked*n

print(part2(test))
print(part2(data))

