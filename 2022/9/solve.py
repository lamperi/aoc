import os.path

FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(FILE) as f:
    INPUT = f.read()

TEST = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

def solve(data, LEN):
    ROPE = [(0,0)]*LEN
    tail_pos = set()
    for line in data.splitlines():
        dir,n = line.split()
        n = int(n)
        dx,dy = {"U": (0,-1), "D": (0,1), "L": (-1,0), "R": (1,0)}[dir]
        for _ in range(n):
            ROPE[0] = ROPE[0][0]+dx, ROPE[0][1]+dy
            for i in range(LEN-1):
                H = ROPE[i]
                T = ROPE[i+1]
                if abs(H[0]-T[0]) > 1 or abs(H[1]-T[1]) > 1:
                    sx = 0 if H[0] == T[0] else (1 if H[0] > T[0] else -1)
                    sy = 0 if H[1] == T[1] else (1 if H[1] > T[1] else -1)
                    ROPE[i+1] = T[0]+sx, T[1]+sy
            tail_pos.add(ROPE[-1])
    return len(tail_pos)

print(solve(TEST, 2), 13)
print(solve(INPUT, 2))
print(solve(TEST, 10), 1)
print(solve("""R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20""", 10), 36)
print(solve(INPUT, 10))
