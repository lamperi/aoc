import sys, operator, functools, binascii
data = open("input.txt").read().strip()

def to_bin(i):
    return i & 0xffff

# Part 1

def func1(a, b, loops=40000000):
    a_factor = 16807
    b_factor = 48271
    mod = 2147483647

    count = 0
    for i in range(loops):
        a = (a*a_factor) % mod
        b = (b*b_factor) % mod

        ab = to_bin(a)
        bb = to_bin(b)
        
        if ab == bb:
            count += 1
    return count
        
# Part 2

def func2(a, b, loops=5000000):
    a_factor = 16807
    b_factor = 48271
    mod = 2147483647

    count = 0
    for i in range(loops):
        while True:
            a = (a*a_factor) % mod
            if a % 4 == 0:
                break
        while True:
            b = (b*b_factor) % mod
            if b % 8 == 0:
                break
        
        ab = to_bin(a)
        bb = to_bin(b)
            
        if ab == bb:
            count += 1
    return count
        
        
print(func1(65, 8921, 5), 1)
print(func2(65, 8921, 1056), 1)

print(func1(65, 8921), 588)
print(func1(512, 191))

print(func2(65, 8921), 309)
print(func2(512, 191))

