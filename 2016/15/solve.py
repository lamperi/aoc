with open("input.txt") as f:
    data = f.read()
    
disks = []
for line in data.splitlines():
    parts = line.split()
    id, num_pos, initial_pos = parts[1], int(parts[3]), int(parts[-1][:-1])
    disks.append((id, num_pos, initial_pos))

print(disks)

def solve(disks):
    
    t = 0
    falling = []
    while True:
        disks = [(id, num_pos, (pos + 1) % num_pos) for id, num_pos, pos in disks]
        falling.append([t,0])
        falling = [(t, i+1) for t,i in falling if disks[i][2] == 0]
        if falling and falling[0][1] == len(disks):
            return falling[0][0]
        t += 1

test_disks = [("#1", 5, 4), ("#2", 2, 1)]

print("TEST:")
print(solve(test_disks))
print("PART 1:")
print(solve(disks))

print("PART 2:")
disks.append(("#7", 11, 0))
print(solve(disks))
