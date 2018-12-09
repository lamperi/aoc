
def solve(players, last_marble):
    marbles = [0]
    index = 0
    scores = [0]*(1+players)
    for marble in range(1, last_marble+1):
        if marble % 23 == 0:
            p = marble%players
            scores[p] += marble
            index -= 7
            if index < 0:
                index = len(marbles)+index
            scores[p] += marbles.pop(index)
        else:
            index += 2
            if index > len(marbles):
                index = 1
            marbles.insert(index, marble)
    return max(scores)

print(solve(9, 25))

print(solve(10, 1618), 8317)
print(solve(13, 7999), 146373)
print(solve(17, 1104), 2764)
print(solve(21, 6111), 54718)
print(solve(30, 5807), 37305)

print(solve(435, 71184))
# Too slow for part 2 due to using non-linked-list
