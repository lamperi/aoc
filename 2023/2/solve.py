import os.path
import math

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def games(data):
    for game in data.splitlines():
        game_id = int(game.split(": ")[0].split()[1])
        subsets = game.split(": ")[1].split(";")
        yield game_id, subsets

def revelations(subsets):
    for subset in subsets:
        bags = subset.split(", ")
        yield {color: int(num) for num, color in (bag.split() for bag in bags)}

def part1(data):
    game_sum = 0
    for game_id, subsets in games(data):
        game_possible = True
        for revelation in revelations(subsets):
            subset_possible = False
            if revelation.get("red", 0) <= 12 and revelation.get("green", 0) <= 13 and revelation.get("blue", 0) <= 14:
                subset_possible = True
            if not subset_possible:
                game_possible = False
                break
        if game_possible:
            game_sum += game_id
    return game_sum

test = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
print(part1(test))
print(part1(data))

def part2(data):
    total_power = 0
    for game_id, subsets in games(data):
        required_cubes = {"red": 0, "blue": 0, "green": 0}
        for revelation in revelations(subsets):
            for color in required_cubes.keys():
                if required_cubes[color] < revelation.get(color, 0):
                    required_cubes[color] = revelation[color]
        power = math.prod(required_cubes.values())
        total_power += power
    return total_power

print(part2(test))
print(part2(data))