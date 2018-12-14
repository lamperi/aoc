from collections import deque


class Recipe:
    def __init__(self, value, prev, next):
        self.value = value
        self.prev = prev
        self.next = next
        self.first = False

def print_recipes(recipe_first, recipe_last, even, odd):
    buf = []
    cur = recipe_first
    while True:
        if cur == even:
            buf.append("({})".format(cur.value))
        elif cur == odd:
            buf.append("[{}]".format(cur.value))
        else:
            buf.append(" {} ".format(cur.value))
        cur = cur.next
        if cur.first:
            break
    print(''.join(buf))

def solve(input):
    recipe_even = Recipe(3, None, None)
    recipe_odd = Recipe(7, None, None)
    recipe_even.prev = recipe_odd
    recipe_even.next = recipe_odd
    recipe_odd.prev = recipe_even
    recipe_odd.next = recipe_even
    recipe_first = recipe_even
    recipe_first.first = True
    recipe_last = recipe_odd

    recipes = 2
    while True:
        cur = recipe_even.value + recipe_odd.value
        for n in str(cur):
            prev_last = recipe_last
            recipe_last = Recipe(int(n), prev_last, recipe_first)
            prev_last.next = recipe_last
            recipe_first.prev = recipe_last
            recipes += 1
        if recipes-10 >= input:
            break

        for _ in range(recipe_even.value+1):
            recipe_even = recipe_even.next
        for _ in range(recipe_odd.value+1):
            recipe_odd = recipe_odd.next
        #print_recipes(recipe_first, recipe_last, recipe_even, recipe_odd)
        
    res = []
    v = recipe_last
    for _ in range(input+10, recipes):
        v = v.prev
    for _ in range(10):
        res.append(str(v.value))
        v = v.prev
    return ''.join(reversed(res))


print(solve(9), 5158916779)
print(solve(5), "0124515891")
print(solve(18), 9251071085)
print(solve(2018), 5941429882)
#print(solve(864801))

def solve2(input):
    recipe_even = Recipe(3, None, None)
    recipe_odd = Recipe(7, None, None)
    recipe_even.prev = recipe_odd
    recipe_even.next = recipe_odd
    recipe_odd.prev = recipe_even
    recipe_odd.next = recipe_even
    recipe_first = recipe_even
    recipe_first.first = True
    recipe_last = recipe_odd

    recipes = 2

    buf = deque([])
    for _ in input:
        buf.append("0")
    while True:
        cur = recipe_even.value + recipe_odd.value
        for n in str(cur):
            prev_last = recipe_last
            recipe_last = Recipe(int(n), prev_last, recipe_first)
            prev_last.next = recipe_last
            recipe_first.prev = recipe_last
            recipes += 1
            buf.append(str(n))
            buf.popleft()
            if ''.join(buf) == input:
                return recipes-len(input)

        for _ in range(recipe_even.value+1):
            recipe_even = recipe_even.next
        for _ in range(recipe_odd.value+1):
            recipe_odd = recipe_odd.next        

print(solve2("51589"), 9)
print(solve2("01245"), 5)
print(solve2("92510"), 18)
print(solve2("59414"), 2018)
# MemoryError
#print(solve2("864801"))