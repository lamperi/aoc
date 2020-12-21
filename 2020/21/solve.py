import os.path
import collections
import re
import math
import itertools
INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

def solve(data):
    foods = []
    for line in data.splitlines():
        ingredients, allergens = line.split(" (")
        ingredients = set(ingredients.split())
        allergens = set(a.rstrip(",") for a in allergens[:-1].split()[1:])
        foods.append(((ingredients, allergens)))

    all_allergens = set()
    all_ingredients = set()
    for ingredients, allergens in foods:
        all_allergens |= allergens
        all_ingredients |= ingredients
    
    can_contain = {}
    # Each allergen is found in exactly one ingredient.
    # Each ingredient contains zero or one allergen
    for allergen in all_allergens:
        can_contain_this = set(all_ingredients)
        for ingredients, allergens in foods:
            if allergen in allergens:
                can_contain_this &= ingredients
        can_contain[allergen] = can_contain_this

    safe = set(all_ingredients)
    for _, ingredients in can_contain.items():
        safe -= ingredients
    s = 0
    for ingredients, _ in foods:
        s += len(ingredients & safe)

    m = {}
    while True:
        for allergen, ingredients in can_contain.items():
            remaining = ingredients - m.keys()
            if len(remaining) == 1:
                remaining_ingredient = next(iter(remaining))
                m[remaining_ingredient] = allergen
        if len(m) == len(all_allergens):
            break
    s2 = ",".join(ing for aller, ing in sorted((aller, ing) for ing, aller in m.items()))

    return "{} {}".format(s, s2)

print(solve("""mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""))
print(solve(data))