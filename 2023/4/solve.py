import os.path

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def part1(data):
    ret = 0
    for line in data.splitlines():
        winning_num, my_num = line.split(": ")[1].split(" | ")
        winning_num = {int(x) for x in winning_num.split()}
        my_num = [int(x) for x in my_num.split()]
        matches = 0
        points_per_card = 1
        for n in my_num:
            if n in winning_num:
                ret += points_per_card
                matches += 1
                if matches > 1:
                    points_per_card *= 2
    return ret

test = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
print(part1(test))
print(part1(data))

def part2(data):
    cards = []
    for line in data.splitlines():
        winning_num, my_num = line.split(": ")[1].split(" | ")
        winning_num = {int(x) for x in winning_num.split()}
        my_num = [int(x) for x in my_num.split()]
        wins = sum(1 for n in my_num if n in winning_num)
        cards.append(wins)
    acc = {}
    for idx, wins in reversed(list(enumerate(cards))):
        acc[idx] = 1
        for w in range(wins):
            acc[idx] += acc[idx+w+1]
    
    return sum(acc.values())

# Override test for part 2.P
# test = """ """

print(part2(test))
print(part2(data))