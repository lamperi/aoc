import os.path
import utils
INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

for i, in utils.ints(data):
    for j, in utils.ints(data):
        if i+j == 2020:
            print(i*j)

for i, in utils.ints(data):
    for j, in utils.ints(data):
        for k, in utils.ints(data):
            if i+j+k == 2020:
                print(i*j*k)
