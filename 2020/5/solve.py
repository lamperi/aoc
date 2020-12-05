import os.path
import collections
import re
import math
INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

def get_seat_id(boarding_pass):
    row = list(range(128))
    for c in boarding_pass[:7]:
        if c == "F":
            row = row[:int(len(row)/2)]
        elif c == "B":
            row = row[int(len(row)/2):]
    row = row[0]
    col = list(range(8))
    for c in boarding_pass[7:]:
        if c == "L":
            col = col[:int(len(col)/2)]
        elif c == "R":
            col = col[int(len(col)/2):]
    col = col[0]
    return row*8+col

def solve(data):
    max_id = 0
    for line in data.splitlines():
        seat_id = get_seat_id(line)
        if seat_id > max_id:
            max_id = seat_id
    return max_id

print(solve("""BFFFBBFRRR"""), 567)
print(solve(data))

def solve2(data):
    seats = set()
    for line in data.splitlines():
        seat_id = get_seat_id(line)
        seats.add(seat_id)
    pos = []
    for seat in range(min(seats), max(seats)):
        if (seat-1) in seats and (seat+1) in seats:
            if seat not in seats:
                pos.append(seat)
    return pos

print(solve2(data))
