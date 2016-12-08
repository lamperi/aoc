import operator as op
import itertools
import copy

with open("input.txt") as file:
    data = file.read()

boss = {}
for line in data.splitlines():
    prop, val = map(str.strip, line.split(":"))
    boss[prop] = int(val)

player = {
    'Hit Points': 50,
    'Armor': 0,
    'Mana': 500,
    'ManaSpent': 0,
    'Effects': {},
    'Cast': []
}

class Spell(object):
    def __init__(self, name, cost, damage = 0, heal = 0, effect_length = 0):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.heal = heal
        self.effect_length = effect_length

    def start(self, player):
        pass
    
    def end(self, player):
        pass
    
    def do_effect(self, player, boss):
        pass
    
    def can_cast(self, player):
        enough_mana = player['Mana'] >= self.cost
        effect_not_active = self.name not in player['Effects']
        return enough_mana and effect_not_active
        
    def cast(self, player, boss):
        player['Mana'] -= self.cost
        player['ManaSpent'] += self.cost
        player['Cast'].append(self.name)

        if self.damage:
            boss['Health'] -= self.damage
            #print("Turn {}: Attacked boss with {}, has now only {} health, attack history = {}".format(len(player['Cast']), self.name, boss['Health'], player['Cast']))
        if self.heal:
            player['Health'] += self.heal
        if self.effect_length:
            #print("Turn {}: Attacked boss with {}, attack history = {}".format(len(player['Cast']), self.name, player['Cast']))
            player['Effects'][self.name] = self.effect_length
            self.start(player)
    
    def on_turn(self, player, boss):
        if self.effect_length and self.name in player['Effects']:
            player['Effects'][self.name] -= 1
            self.do_effect(player, boss)
            if player['Effects'][self.name] == 0:
                del player['Effects'][self.name]
                self.end(player)
                
    def __str__(self):
        return self.name

class MagicMissile(Spell):
    def __init__(self):
        super(MagicMissile, self).__init__('Magic Missile', 53, damage = 4)

class Drain(Spell):
    def __init__(self):
        super(Drain, self).__init__('Drain', 73, damage = 2, heal = 2)
        
class Shield(Spell):
    def __init__(self):
        super(Shield, self).__init__('Shield', 113, effect_length = 6)
    
    def start(self, player):
        player['Armor'] = 7
        
    def end(self, player):
        player['Armor'] = 0

class Poison(Spell):
    def __init__(self):
        super(Poison, self).__init__('Poison', 173, effect_length = 6)
        
    def do_effect(self, player, boss):
        boss['Health'] -= 3

class Recharge(Spell):
    def __init__(self):
        super(Recharge, self).__init__('Recharge', 229, effect_length = 5)

    def do_effect(self, player, boss):
        player['Mana'] += 101

def attack(attacker, defender):
    #print("Before attack we have {} health".format(defender['Health']))
    defender['Health'] -= max(1, attacker['Damage'] - defender['Armor'])
    #print("After attack we have {} health".format(defender['Health']))

spells = [MagicMissile(), Drain(), Shield(), Poison(), Recharge()]

def simulate_battles(player, boss, spells, hard_mode):
    player = dict(player)
    boss = dict(boss)
    player['Health'] = player['Hit Points']
    boss['Health'] = boss['Hit Points']
    for solution in simulate_turns(player, boss, spells, hard_mode):
        yield solution

def simulate_turns(player, boss, spells, hard_mode):
    if player['ManaSpent'] >= (1300 if hard_mode else 1000):
        return
    for cast_spell in spells:
        copy_player = copy.deepcopy(player)
        copy_boss = dict(boss)
        for solution in simulate_turn(copy_player, copy_boss, cast_spell, spells, hard_mode):
            yield solution

def simulate_turn(player, boss, cast_spell, spells, hard_mode):
    # HARD MODE
    if hard_mode:
        player['Health'] -= 1
        if player['Health'] <= 0:
            return
    
    # PLAYER CASTS SPELL
    for spell in spells:
        spell.on_turn(player, boss)
    if boss['Health'] <= 0:
        yield player
        return

    if not cast_spell.can_cast(player):
        # This game is actually impossible
        return
    
    cast_spell.cast(player, boss)
    
    if boss['Health'] <= 0:
        yield player
        return
        
    # BOSS ATTACKS
    for spell in spells:
        spell.on_turn(player, boss)
    if boss['Health'] <= 0:
        yield player
        return
    attack(boss, player)
    if player['Health'] <= 0:
        return
    
    # MORE TURNS!
    for solution in simulate_turns(player, boss, spells, hard_mode):
        yield solution

def solve(player, boss, spells, hard_mode=False):
    player = copy.deepcopy(player)
    boss = copy.deepcopy(boss)
    min_cost = None
    min_solution = None
    for solution in simulate_battles(player, boss, spells, hard_mode):
        cost = solution['ManaSpent']
        #print("Solution with {} mana spent using spells = {}".format(cost, solution['Cast']))
        if min_cost is None or cost < min_cost:
             min_cost = cost
             min_solution = solution
    if min_cost:
        print("*"*50)
        print("Win with {} mana spent using spells = {}".format(min_cost, min_solution['Cast']))
        print("*"*50)

# TEST
def test1(player, boss, spells):
    player = copy.deepcopy(player)
    boss = copy.deepcopy(boss)
    player['Hit Points']=10
    player['Mana']=250
    boss['Hit Points']=13
    boss['Damage']=8
    print("*** TEST 1: ")
    solve(player, boss, spells)

def test2(player, boss, spells):
    player = copy.deepcopy(player)
    boss = copy.deepcopy(boss)
    player['Hit Points']=10
    player['Mana']=250
    boss['Hit Points']=14
    boss['Damage']=8
    print("*** TEST 2: ")
    solve(player, boss, spells)
    
test1(player, boss, spells)
test2(player, boss, spells)

print("*** PART 1: ")
solve(player, boss, spells)

print("*** PART 2: ")
solve(player, boss, spells, True)