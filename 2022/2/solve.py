import os.path

FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(FILE) as f:
    INPUT = f.read()

TEST = """A Y
B X
C Z"""

def solve(data):
    scores = {
        "X": 1,
        "Y": 2,
        "Z": 3,
    }
    outcomes = {
        "X": {
            "A": 3, "B": 0, "C": 6
        },
        "Y": {
            "A": 6, "B": 3, "C": 0,
        },
        "Z": {
            "A": 0, "B": 6, "C": 3,
        }
    }
    score = 0
    for line in data.splitlines():
        elf, me = line.split()
        score += outcomes[me][elf] + scores[me]
    return score

print(solve(TEST))
print(solve(INPUT))

def solve2(data):
    outcomes = {
        "X": 0,
        "Y": 3,
        "Z": 6,
    }
    scores = {
        "X": {
            "A": 3, "B": 1, "C": 2
        },
        "Y": {
            "A": 1, "B": 2, "C": 3,
        },
        "Z": {
            "A": 2, "B": 3, "C": 1,
        }
    }
    score = 0
    for line in data.splitlines():
        elf, me = line.split()
        score += scores[me][elf] + outcomes[me]
    return score

print(solve2(TEST))
print(solve2(INPUT))