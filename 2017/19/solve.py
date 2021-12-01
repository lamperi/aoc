example = """     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ 
"""

import os.path
INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

# Part 1


def func(data):
    # find start
    maze = []
    for line in data.splitlines():
        maze.append(line)
    pos = None
    dir = None
    for i, c in enumerate(maze[0]):
        if c != ' ':
            pos = (0, i)
            dir = (1, 0)
            break

    # Search
    letters = []
    steps = 0
    while True:
        steps += 1
        old_pos = pos
        next_y = pos[0] + dir[0]
        next_x = pos[1] + dir[1]
        next_c = maze[next_y][next_x] if 0 <= next_y < len(maze) and 0 <= next_x < len(maze[next_y]) else ' '
        if next_c != ' ':
            pos = (next_y, next_x)
            if next_c.isalpha():
                letters.append(next_c)
        else:
            if dir[0] == 0:
                new_dirs = [(-1, 0), (1, 0)]
            else:
                new_dirs = [(0, -1), (0, 1)]
            for new_dir in new_dirs:
                next_y = pos[0] + new_dir[0]
                next_x = pos[1] + new_dir[1]
                next_c = maze[next_y][next_x] if 0 <= next_y < len(maze) and 0 <= next_x < len(maze[next_y]) else ' '
                if next_c != ' ':
                    pos = (next_y, next_x)
                    dir = new_dir
                    if next_c.isalpha():
                        letters.append(next_c)
                    break
        if old_pos == pos:
            break
    return "".join(letters), steps


print(func(example))
print(func(data))