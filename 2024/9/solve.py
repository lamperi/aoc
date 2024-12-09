import os.path
from collections import deque

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

def part2(data):
    disk_map = []
    for _, c in enumerate(data.rstrip()):
        disk_map.append(int(c))
        
    disk = []
    free_space = deque()
    for i, c in enumerate(disk_map):
        if i % 2 == 0:
            file_id = i//2
            disk.append((c, file_id))
        else:
            disk.append((c, -1))
            free_space.append(c)
    disk_index = len(disk) - 1

    while disk_index > 0:
        size, file_id = disk[disk_index]
        if file_id == -1:
            disk_index -= 1
            continue
        #print_disk(disk)
        
        begin_index = 0
        moved = False
        while not moved and begin_index < disk_index:
            other_size, other_file_id = disk[begin_index]
            if other_file_id != -1 or other_size < size:
                begin_index += 1
                continue
            
            if other_size == size:
                disk[disk_index] = (size, other_file_id)
                disk[begin_index] = (size, file_id)
                moved = True
                break
            elif other_size > size:
                disk[begin_index] = (size, file_id)
                disk[disk_index] = (size, -1)
                disk.insert(begin_index + 1, (other_size - size, -1))
                disk_index += 1
                moved = True
                break
        disk_index -= 1

    idx = 0
    s = 0
    for size, file_id in disk:
        if file_id != -1:
            for _ in range(size):
                s += idx * file_id
                idx += 1
        else:
            idx += size
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