import operator as op
import itertools
import copy

with open("input.txt") as file:
    data = file.read()

packages = map(int, data.splitlines())

N=len(packages)
print("N={}, sum={}, data={}".format(N, sum(packages), packages))

def solve1():
    def sizes(N,min_a=1):
        for a in range(min_a, 1+int(N/3)):
            for b in range(a, 1+int((N-a)/2)):
                c  = N - a - b
                yield (a,b,c)            
        
    min_a = 0
    target_sum = sum(packages)/3
    for i in range(1,N/3):
        if sum(packages[-i:]) > target_sum:
            min_a = i
            break
    print("Size of smallest group must be at least {}".format(target_sum)) 
    
    min_PA = None
    for a,b,c in sizes(N, min_a = min_a):
        print("Testing {},{},{}".format(a,b,c))
        for A in itertools.combinations(packages, a):
            sumA = sum(A)
            if sumA == target_sum:
                packages2 = [package for package in packages if package not in A]
                for B in itertools.combinations(packages2, b):
                    if sum(B) == target_sum:
                        PA = reduce(op.mul, A, 1)
                        if min_PA is None or PA < min_PA:
                            print("New minimum: {} for A ={}".format(PA, A))
                            min_PA = PA
                    
    print("PART 1: {}".format(min_PA))

def solve2():
    def sizes(N,min_a=1):
        for a in range(min_a, 1+int(N/4)):
            for b in range(a, 1+int((N-a)/3)):
                for c in range(b, 1+int((N-a-b)/2)):
                    d  = N - a - b - c
                    yield (a,b,c,d)            
    min_a = 0
    target_sum = sum(packages)/4
    for i in range(1,N/4):
        if sum(packages[-i:]) > target_sum:
            min_a = i
            break
    print("Size of smallest group must be at least {}".format(min_a))
    
    min_PA = None
    for a,b,c,d in sizes(N, min_a = min_a):
        print("Testing {},{},{},{}".format(a,b,c,d))
        for A in itertools.combinations(packages, a):
            if sum(A) == target_sum:
                packages2 = [package for package in packages if package not in A]
                for B in itertools.combinations(packages2, b):
                    if sum(B) == target_sum:
                        packages3 = [package for package in packages2 if package not in B]
                        for C in itertools.combinations(packages2, c):
                            if sum(C) == target_sum:
                                PA = reduce(op.mul, A, 1)
                                if min_PA is None or PA < min_PA:
                                    print("New minimum: {} for A ={}".format(PA, A))
                                    min_PA = PA
                    
    print("PART 2: {}".format(min_PA))

solve1() 
solve2()