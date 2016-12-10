import operator as op
import itertools
import copy

with open("input.txt") as file:
    data = file.read()

key_row, key_column = [int(w) for w in data.replace(",","").replace(".","").split() if w.isdigit()]

def generate_codes():
    code = 20151125
    row = 1
    column = 1
    yield (code, row, column)
    while True:
        code = (code * 252533) % 33554393
        if row == 1:
            row, column = column + 1, 1
        else:
            row, column = row - 1, column + 1
        yield(code, row, column)


for code,row,column in generate_codes():
    if row == key_row and column == key_column:
        print("PART 1: {} at {},{}".format(code, row, column))
        break
print("PART 2 ... just click the link to get the last star!")