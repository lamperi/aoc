import os.path
from collections import deque
from dataclasses import dataclass

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def part1(data):
    disk_map = []
    for _, c in enumerate(data.rstrip()):
        disk_map.append(int(c))
        
    disk = []
    free_space = deque()
    idx = 0
    for i, c in enumerate(disk_map):
        if i % 2 == 0:
            file_id = i//2
            for _ in range(c):
                disk.append(file_id)
                idx += 1
        else:
            for _ in range(c):
                disk.append(-1)
                free_space.append(idx)
                idx += 1

    last_index = len(disk) - 1
    while free_space and last_index >= 0:
        while disk[last_index] == -1:
            last_index -= 1
        idx = free_space.popleft()
        if idx > last_index:
            break
        disk[idx], disk[last_index] = disk[last_index], disk[idx]
        last_index -= 1

    return sum(i* file_id for i, file_id in enumerate(disk) if file_id != -1)

test = """2333133121414131402"""
print(part1(test))
print(part1(data))

@dataclass
class File:
    file_id: int
    start_position: int
    size: int

def part2(data):
    disk_map = []
    for _, c in enumerate(data.rstrip()):
        disk_map.append(int(c))
        
    files = []
    free_spaces = []
    position = 0
    for i, size in enumerate(disk_map):
        if i % 2 == 0:
            file_id = i//2
            files.append(File(file_id, position, size))
        else:
            free_spaces.append(File(-1, position, size))
        position += size
    
    first_with_capacity = 0
    for file_to_defrag in reversed(files):
        for idx, free_space in enumerate(free_spaces[first_with_capacity:], start=first_with_capacity):
            if free_space.start_position > file_to_defrag.start_position:
                break
            if free_space.size >= file_to_defrag.size:
                free_space.size -= file_to_defrag.size
                file_to_defrag.start_position = free_space.start_position
                free_space.start_position += file_to_defrag.size
                if idx == first_with_capacity:
                    while free_spaces[first_with_capacity].size == 0:
                        first_with_capacity += 1
                break

    s = 0
    for file in files:
        s += file.size * (file.start_position + file.start_position + file.size - 1)//2 * file.file_id
    return s

def print_disk(disk):
    s = ""
    for size, c in disk:
        s += size * (str(c) if c != -1 else ".")
    print(s)

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))
