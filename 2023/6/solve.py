import os.path
import math

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def closed_form_solution(time, distance):
    # The function is (time-x)*x >= distance
    # It is actually a 2nd order function of form -x*2 + time*x - distance > 0
    # The solutions are given by:
    # (-b +- sqrt(b^2 - 4ac))/2a
    low = (-time + (time*time - 4*distance)**0.5)/-2
    hi = (-time - (time*time - 4*distance)**0.5)/-2
    # If the roots are integers, we don't want them into our range.
    if hi - round(hi) < 1e-10:
        hi -= 0.1
    if low - round(low) < 1e-10:
        low += 0.1
    # Take floor of hi and ceil of low, then add 1
    # because we are dealing here with integers.
    return math.floor(hi) - math.ceil(low) + 1


def part1(data):
    time, distance, *_ = data.splitlines()
    time = [int(x) for x in time.split()[1:]]
    distance = [int(x) for x in distance.split()[1:]]
    
    s = []
    for t, d in zip(time, distance):
        y = 0
        for hold in range(t):
            dist = (t-hold)*hold
            if dist > d:
                y += 1
        s.append(y)
    return math.prod(s)

def part1_analytic(data):
    time, distance, *_ = data.splitlines()
    time = [int(x) for x in time.split()[1:]]
    distance = [int(x) for x in distance.split()[1:]]
    
    s = []
    for t, d in zip(time, distance):
        s.append(closed_form_solution(t, d))
    return math.prod(s)


test = """Time:      7  15   30
Distance:  9  40  200"""
print(part1(test))
print(part1(data))

print(part1_analytic(test))
print(part1_analytic(data))

def part2(data):
    time, distance, *_ = data.splitlines()
    time = int("".join([x for x in time.split()[1:]]))
    distance = int("".join([x for x in distance.split()[1:]]))
    
    y = 0
    for hold in range(time):
        dist = (time-hold)*hold
        if dist > distance:
            y += 1
    return y


def part2_analytic(data):
    time, distance, *_ = data.splitlines()
    time = int("".join([x for x in time.split()[1:]]))
    distance = int("".join([x for x in distance.split()[1:]]))
    return closed_form_solution(time, distance)

# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))

print(part2_analytic(test))
print(part2_analytic(data))
