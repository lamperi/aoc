import sys
data = open("input.txt").read().strip()

def checksum(data):
    csum = 0
    for line in data.splitlines():
        numbers = [int(s) for s in line.split()]
        check = max(numbers) - min(numbers)
        csum += check
    return csum

print(checksum("""5 1 9 5
7 5 3
2 4 6 8"""))

print(checksum(data))


def sub(numbers):
    for i, n in enumerate(numbers):
        for m in numbers[i+1:]:
            if n % m == 0:
                return n / m
            elif m % n == 0:
                return m / n            

def checksum2(data):
    csum = 0
    for line in data.splitlines():
        numbers = [int(s) for s in line.split()]
        check = sub(numbers)
        csum += check
    return csum

print(checksum2("""5 9 2 8
9 4 7 3
3 8 6 5"""))

print(checksum2(data))