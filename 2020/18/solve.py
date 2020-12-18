import os.path
import collections
import re
import math
import itertools
INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()


testdata = """1 + 2 * 3 + 4 * 5 + 6
1 + (2 * 3) + (4 * (5 + 6))
2 * 3 + (4 * 5)
5 + (8 * 3 + 9 + 3 * 4 * 3)
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"""

## Abuse Python AST

import ast

def eval_part1(module):
    def eval(expr):
        if isinstance(expr, ast.Constant):
            return expr.value
        assert isinstance(expr, ast.BinOp)
        if isinstance(expr.op, ast.Sub):
            return eval(expr.left) * eval(expr.right)
        elif isinstance(expr.op, ast.Add):
            return eval(expr.left) + eval(expr.right)
        else:
            assert False
    assert len(module.body) == 1
    return eval(module.body[0].value)

def solve_part1(data):
    s = 0
    for line in data.splitlines():
        line = line.replace("*", "-")
        expr = ast.parse(line)
        v = eval_part1(expr)
        s += v
    return s

def eval_part2(module):
    def eval(expr):
        if isinstance(expr, ast.Constant):
            return expr.value
        if isinstance(expr.op, ast.Sub):
            return eval(expr.left) * eval(expr.right)
        elif isinstance(expr.op, ast.Div):
            return eval(expr.left) + eval(expr.right)
        else:
            assert False
    assert len(module.body) == 1
    return eval(module.body[0].value)

def solve_part2(data):
    s = 0
    for line in data.splitlines():
        line = line.replace("*", "-")
        line = line.replace("+", "/")
        expr = ast.parse(line)
        v = eval_part2(expr)
        s += v
    return s

print(solve_part1(testdata))
print(solve_part1(data))
print(solve_part2(testdata))
print(solve_part2(data))
