import pathlib
import re
import itertools
from dataclasses import dataclass
from typing import Set
inputPath = pathlib.Path(__file__).parent.joinpath('input.txt')
data = inputPath.read_text()

example = """Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4"""

@dataclass
class UnitGroup:
	units: int
	hit_points: int
	attack: int
	initiative: int
	damage_type: str
	weaknesses: Set[str]
	immunities: Set[str]
	side: str
	group_number: int
	next_target = None
	selected: bool = False

	def effective_power(self):
		return self.units * self.attack

def select_targets(groups, enemy_groups, debug):
	for group in sorted(groups, key = lambda group: (-group.effective_power(), -group.initiative)):
		best_target_criteria = (0, 0, 0)
		best_target = None
		for target in enemy_groups:
			if target.selected:
				continue
			dmg = group.effective_power()
			if group.damage_type in target.immunities:
				dmg = 0
			elif group.damage_type in target.weaknesses:
				dmg *= 2
			target_criteria = (dmg, target.effective_power(), target.initiative)
			if dmg > 0 and target_criteria > best_target_criteria:
				best_target_criteria = target_criteria
				best_target = target
			if debug:
				print("{} group {} would deal defending group {} {} damage".format(
					group.side, group.group_number, target.group_number, dmg))
		if best_target:
			best_target.selected = True
			group.next_target = best_target


def attack(groups, debug):
	total_killed = 0
	for group in sorted(groups, key = lambda group: (-group.initiative)):
		target = group.next_target
		if not target:
			continue
		dmg = group.effective_power()
		if group.damage_type in target.immunities:
			dmg = 0
		elif group.damage_type in target.weaknesses:
			dmg *= 2
		killed, _ = divmod(dmg, target.hit_points)
		if killed > target.units:
			killed = target.units
		target.units -= killed
		total_killed += killed
		if debug:
			print("{} group {} attacks defending group {}, killing {} units"
				.format(group.side, group.group_number, target.group_number, killed))
	if debug:
		print()
	return total_killed

def parse_input(input_data, boost):
	immune_system = []
	infection = []
	current = None
	side = None
	for line in input_data.splitlines():
		if line == 'Immune System:':
			current = immune_system
			side = 'Immune System'
		elif line == 'Infection:':
			current = infection
			side = 'Infection'
		elif line:
			nums = list(map(int, re.findall(r'-?\d+', line)))
			attack_type = re.findall(r'\w+ damage', line)[0].split()[0]
			weaknesses = set()
			immunities = set()
			w = re.findall(r'weak to [a-z, ]+', line)
			if w:
				weaknesses = set(w[0][len('weak to '):].split(", "))
			i = re.findall(r'immune to [a-z, ]+', line)
			if i:
				immunities = set(i[0][len('immune to '):].split(", "))
			

			units, hit_points, attack, initiative = nums
			if side == 'Immune System':
				attack += boost
			group = UnitGroup(units, hit_points, attack, initiative, attack_type, weaknesses, immunities, side, len(current)+1)
			current.append(group)
	return immune_system, infection

def solve(input_data, boost, debug=False):
	immune_system, infection = parse_input(input_data, boost)
	groups = immune_system + infection
	for _ in itertools.count():
		if debug:
			print('Immune System:')
			if not immune_system:
				print('No groups remaining.')
			for group in immune_system:
				print("Group {} contains {} units.".format(group.group_number, group.units))
			print('Infection:')
			if not infection:
				print('No groups remaining.')
			for group in infection:
				print("Group {} contains {} units.".format(group.group_number, group.units))
			print()
		if boost == 0 and (not immune_system or not infection):
			return sum(group.units for group in groups)
		elif boost > 0 and (not immune_system or not infection):
			return sum(group.units for group in immune_system)
		# Target selection
		# Clear old targets
		for group in groups:
			group.next_target = None
			group.selected = False
		select_targets(infection, immune_system, debug)
		select_targets(immune_system, infection, debug)
		if debug:
			print()
		# Attacking
		killed = attack(groups, debug)
		if killed == 0:
			return 0

		immune_system = [group for group in immune_system if group.units > 0]
		infection = [group for group in infection if group.units > 0]
		groups = immune_system + infection
	return

ans = solve(example, 0, False)
assert ans == 5216

ans = solve(data, 0, False)
assert ans == 13331
print(ans)

ans = solve(example, 1570, False)
assert ans == 51

def part2_solve(input_data, debug):
	for boost in itertools.count(1):
		ans = solve(data, boost, debug)
		if ans > 0:
			return ans

ans = part2_solve(example, False)
assert ans == 7476
print(ans)