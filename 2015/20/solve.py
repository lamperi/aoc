target = 36000000
present_per_house = 10

import time
def print_time(func):
    def wrapper():
        start = time.time()
        func()
        end = time.time()
        print("Function {} took {:.2} s".format(func.__name__, int(end-start)))
    return wrapper

@print_time
def part1bruteforce():
    # PART 1
    # Slow method - brute force
    # start and inc values by guessing
    start = 327600
    inc = int(2**3 * 3*2)
    
    current_best = 0
    for house in xrange(start, target, inc):
        house_score = sum(elf * present_per_house for elf in xrange(1, house+1) if house % elf == 0)
        if house_score >= target:
            print("PART 1: Target house is {}".format(house))
            break
        #if house_score > current_best:
        #    current_best = house_score
        #    print("Found new high score: {} for house {}".format(current_best, house))

@print_time
def part1guess():
    # PART 1 - generate good guesses
    def generate_factorized():
        """
        Generates numbers that have a lot of factors
        """
        limit = target / 10
        for a in xrange(12):
            #print("a={}".format(a))
            aa = 2**a
            if aa >= limit:
                break
            for b in xrange(5):
                bb = aa * 3**b
                if bb >= limit:
                    break
                for c in xrange(4):
                    cc = bb * 5**c
                    if cc >= limit:
                        break
                    for d in xrange(3):
                        dd = cc * 7**d
                        if dd >= limit:
                            break
                        for e in xrange(2):
                            ee = dd * 11*e
                            if ee >= limit:
                                break
                            for f in xrange(1):
                                ff = ee * 13**f
                                if ff >= limit:
                                    break
                                else:
                                    yield ff
                                 
    
    scores = sorted([(sum(elf * present_per_house for elf in xrange(1, house+1) if house % elf == 0), house) for house in generate_factorized()])
    for house_score, house in scores:
        if house_score >= target:
            print("PART 1: Target house {} has score {}".format(house, house_score))
            break

@print_time
def part1fast():
    # PART 1 sieve like
    max_guess = 1000000
    presents = [0]*max_guess
    
    for elf in xrange(1, max_guess):
        for house in xrange(elf, max_guess, elf):
            if house < max_guess:
                presents[house] += elf * present_per_house
    
    for house,house_score in enumerate(presents):
        if house_score >= target:
            print("PART 1: Target house {} has score {}".format(house, house_score))
            break

@print_time
def part2fast():
    # PART 2 sieve like
    present_per_house = 11
    max_guess = 1000000
    presents = [0]*max_guess
    
    for elf in xrange(1, max_guess):
        for house_id in xrange(1, 51):
            house = elf*house_id
            if house < max_guess:
                presents[house] += elf * present_per_house
    
    for house,house_score in enumerate(presents):
        if house_score >= target:
            print("PART 2: Target house {} has score {}".format(house, house_score))
            break



part1fast()
part2fast()
part1guess()
part1bruteforce()