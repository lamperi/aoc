import os.path
import collections
import re
import math
import time
import itertools
from timeit import default_timer as timer
INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

def solve(data):
    a, b = data.strip().splitlines()
    card_public_key = int(a)
    door_public_key = int(b)

    value = 1
    loop = 0
    while value != card_public_key:
        loop += 1
        value *= 7
        value = value % 20201227
    card_loop = loop
    print("Card loop", card_loop)

    value = 1
    loop = 0
    while value != door_public_key:
        loop += 1
        value *= 7
        value = value % 20201227
    door_loop = loop
    print("Door loop", door_loop)

    value = 1
    for loop in range(door_loop):
        value *= card_public_key
        value = value % 20201227
    print("Card encyption key", value)

    value = 1
    for loop in range(card_loop):
        value *= door_public_key
        value = value % 20201227
    print("Door encyption key", value)

    return value


print(solve("""17807724
5764801"""))
print(solve(data))