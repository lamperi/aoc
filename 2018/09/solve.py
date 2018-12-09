from collections import deque

def solve_deque(players, last_marble):
    marbles = deque([0])
    scores = [0]*(1+players)
    for marble in range(1, last_marble+1):
        if marble % 23 == 0:
            p = marble%players
            scores[p] += marble
            marbles.rotate(7)
            scores[p] += marbles.popleft()
        else:
            marbles.rotate(-2)
            marbles.appendleft(marble)
    return max(scores)

print(solve_deque(9, 25))
print(solve_deque(10, 1618), 8317)
print(solve_deque(13, 7999), 146373)
print(solve_deque(17, 1104), 2764)
print(solve_deque(21, 6111), 54718)
print(solve_deque(30, 5807), 37305)

print(solve_deque(435, 71184))
print(solve_deque(435, 71184*100))
