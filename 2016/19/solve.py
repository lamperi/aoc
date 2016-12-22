def part1_naive_solve(n):
    """
    Bruteforce solution:
    Iterate all elves and remove next by marking it False.
    """
    elves = [True]*n
    state = 0
    cnt = n
    while True:
        for i in xrange(n):
            if state == 0:
                if elves[i]:
                    state = 1
                    if cnt == 1:
                        return i+1
            elif state == 1:
                if elves[i]:
                    elves[i] = False
                    state = 0
                    cnt -= 1

def solve_part1(n):
    solution = part1_naive_solve(n)
    print("Part 1: Solution: {}".format(solution))

def part2_solve(n):
    """
    Solve by two moving iterators.
    First one moves the "current" elv, other moves the elv to be deleted.
    """
    # Create elves
    elves = [{"value": i+1} for i in range(n)]
    for prev_elv,elv,next_elv in zip([elves[-1]] + elves[:-1], elves, elves[1:] + [elves[0]]):
        elv["previous"] = prev_elv
        elv["next"] = next_elv
    iter_elv = elves[0]
    iter_remove = elves[len(elves)/2]
    cnt = n
    while cnt > 1:
         iter_remove["next"]["previous"] = iter_remove["previous"]
         iter_remove["previous"]["next"] = iter_remove["next"]
         iter_remove = iter_remove["next"]
         iter_elv = iter_elv["next"]
         cnt -= 1
         # If we have even number of elves after delete, move again
         # -> otherwise the remove iterator gets left behind
         if cnt % 2 == 0:
             iter_remove = iter_remove["next"]
    return iter_elv["value"]

def solve_part2(n):
    solution = part2_solve(n)
    print("Part 2: Solution: {}".format(solution))

def test():    
    print("3 == {}".format(part1_naive_solve(5)))
    print("2 == {}".format(part2_solve(5)))
    
    
if __name__ == "__main__":
    test()     
 
    n = 3001330
    solve_part1(n)
    solve_part2(n)