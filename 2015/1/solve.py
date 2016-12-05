with open("input.txt") as file:
    data = file.read()

# PART 1    
floor = data.count("(") - data.count(")")
print(floor)

# PART 2
floor = 0
for index, inst in enumerate(data):
    floor += 1 if inst == "(" else -1
    if floor < 0:
        print(index + 1)
        break
