import os.path
from enum import Enum
from collections import Counter

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

class Hand:
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1

def score(card):
    match card:
        case 'A': return 14
        case 'K': return 13
        case 'Q': return 12
        case 'J': return 11
        case 'T': return 10
        case n: return int(n)

def hand_score(hand):
    cards, _ = hand
    scores = [score(c) for c in cards]
    cnt = Counter(cards)
    match cnt.most_common():
        case [(_, 5)]: return (Hand.FIVE_OF_A_KIND, scores)
        case [(_, 4), _]: return (Hand.FOUR_OF_A_KIND, scores)
        case [(_, 3), (_, 2)]: return (Hand.FULL_HOUSE, scores)
        case [(_, 3), _, _]: return (Hand.THREE_OF_A_KIND, scores)
        case [(_, 2), (_, 2), _]: return (Hand.TWO_PAIR, scores)
        case [[_, 2], _, _, _]: return (Hand.ONE_PAIR, scores)
        case [_, _, _, _, _]: return (Hand.HIGH_CARD, scores)


def part1(data):
    hands = [line.split() for line in data.splitlines()]
    hands.sort(key=hand_score)
    s = 0
    for multiplier, (_, score) in enumerate(hands, start=1):
        s += multiplier * int(score)
    return s

test = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""
print(part1(test))
print(part1(data))

def score_part2(card):
    match card:
        case 'A': return 14
        case 'K': return 13
        case 'Q': return 12
        case 'J': return 1
        case 'T': return 10
        case n: return int(n)

def hand_score_part2(hand):
    cards, _ = hand
    scores = [score_part2(c) for c in cards]
    
    if 'J' in cards:
        non_jokers = set(cards) - {'J'}
        if not non_jokers:
            return (Hand.FIVE_OF_A_KIND, scores)
        cnt = Counter(cards)
        for c, _ in cnt.most_common():
            if c != 'J':
                jokers_target = c
                break
        cards = cards.replace('J', jokers_target)

    cnt = Counter(cards)
    match cnt.most_common():
        case [(_, 5)]: return (Hand.FIVE_OF_A_KIND, scores)
        case [(_, 4), _]: return (Hand.FOUR_OF_A_KIND, scores)
        case [(_, 3), (_, 2)]: return (Hand.FULL_HOUSE, scores)
        case [(_, 3), _, _]: return (Hand.THREE_OF_A_KIND, scores)
        case [(_, 2), (_, 2), _]: return (Hand.TWO_PAIR, scores)
        case [[_, 2], _, _, _]: return (Hand.ONE_PAIR, scores)
        case [_, _, _, _, _]: return (Hand.HIGH_CARD, scores)

def part2(data):
    hands = [line.split() for line in data.splitlines()]
    hands.sort(key=hand_score_part2)
    s = 0
    for multiplier, (_, score) in enumerate(hands, start=1):
        s += multiplier * int(score)
    return s

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))