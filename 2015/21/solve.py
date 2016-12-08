import operator as op
import itertools

with open("input.txt") as file:
    data = file.read()

shop = """Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3
"""
weapons = []
armors = []
rings = []
current = None
for line in shop.splitlines():
    if "Weapons:" in line:
        current = weapons
    elif "Armor:" in line:
        current = armors
    elif "Rings:" in line:
        current = rings
    elif line == "":
        current = None
    else:
        name, cost, damage, armor = line.rsplit(None, 3)
        current.append([name, int(cost), int(damage), int(armor)])

boss = {}
for line in data.splitlines():
    prop, val = map(str.strip, line.split(":"))
    boss[prop] = int(val)

player = {
    'Hit Points': 100,
    'Damage': 0,
    'Armor': 0
}

def attack(attacker, defender):
    defender['Health'] -= max(1, attacker['Damage'] - defender['Armor'])
    
def simulate_battle(player, boss):
    player['Health'] = player['Hit Points']
    boss['Health'] = boss['Hit Points']
    for turn in range(max(map(op.itemgetter('Hit Points'), (player, boss)))):
        attack(player, boss)
        if boss['Health'] <= 0:
            return True
        attack(boss, player)
        if player['Health'] <= 0:
            return False
            
    raise Exception("Battle did not end")

def generate_gear(weapons, armors, rings):
    for weapon in weapons:
        for armor in itertools.chain([None], armors):
            for ring1, ring2 in itertools.combinations(rings, 2):
                yield (weapon, armor, ring1, ring2)
            for ring1 in rings:
                yield (weapon, armor, ring1, None)
            yield (weapon, armor, None, None)

def solve():
    min_cost_to_win = None
    max_cost_to_lose = None
    for weaponStats, armorStats, ring1Stats, ring2Stats in generate_gear(weapons, armors, rings):
        gear_name = [gear[0] for gear in [weaponStats, armorStats, ring1Stats, ring2Stats] if gear is not None]
        cost, damage, armor = reduce(lambda a,b: [a[0] + b[0], a[1] + b[1], a[2] + b[2]], [gear[1:] for gear in [weaponStats, armorStats, ring1Stats, ring2Stats] if gear is not None], [0,0,0])
        player['Damage'] = damage
        player['Armor'] = armor
        player_wins = simulate_battle(player, boss)
        if player_wins and (min_cost_to_win is None or cost < min_cost_to_win):
            min_cost_to_win = cost
            print("Cheaper equipment with win condition, cost={}, damage={}, armor={}, gear={}".format(cost, damage, armor, gear_name))
            #print("Stats {}, {}, {}, {}".format(weaponStats, armorStats, ring1Stats, ring2Stats))
        if not player_wins and (max_cost_to_lose is None or cost > max_cost_to_lose):
            max_cost_to_lose = cost
            print("More expensive equipment with lose condition, cost={}, damage={}, armor={}, gear={}".format(cost, damage, armor, gear_name))
solve()