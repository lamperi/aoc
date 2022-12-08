import os.path
import re

FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(FILE) as f:
    INPUT = f.read()

TEST = """30373
25512
65332
33549
35390"""

def gen_trees(grid, i, j, di, dj):
    ii = i+di
    jj = j+dj
    while 0 <= ii < len(grid) and 0 <= jj < len(grid[i]):
        yield grid[ii][jj]
        jj += dj
        ii += di

def solve(data):
    grid = data.splitlines()
    visible = 0  # PART 1
    max_scenic_score = 0  # PART 2
    for i, row in enumerate(grid):
        for j, tree in enumerate(row):
            is_visible = False
            scenic_score = 1
            for di, dj in ((-1,0), (0, 1), (1, 0), (0, -1)):
                # PART 1
                if all(t < tree for t in gen_trees(grid, i, j, di, dj)):
                    is_visible = True
                # PART 2
                visible_in_direction = 0
                for t in gen_trees(grid, i, j, di, dj):
                    visible_in_direction += 1
                    if t >= tree:
                        break
                scenic_score *= visible_in_direction
            # PART 1
            if is_visible:
                visible += 1
            # PART 2
            if scenic_score > max_scenic_score:
                max_scenic_score = scenic_score
    return visible, max_scenic_score

print(solve(TEST))
print(solve(INPUT))
