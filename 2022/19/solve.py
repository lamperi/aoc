import os.path
from itertools import pairwise
import re

FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(FILE) as f:
    INPUT = f.read()

def ints(line):
    return map(int, re.findall("-?\d+", line))

TEST = """Blueprint 1:
  Each ore robot costs 4 ore.
  Each clay robot costs 2 ore.
  Each obsidian robot costs 3 ore and 14 clay.
  Each geode robot costs 2 ore and 7 obsidian.

Blueprint 2:
  Each ore robot costs 2 ore.
  Each clay robot costs 3 ore.
  Each obsidian robot costs 3 ore and 8 clay.
  Each geode robot costs 3 ore and 12 obsidian."""


def solve(data, part):
    blueprints = data.split('\n\n') 
    if len(blueprints) == 1:
      blueprints = data.splitlines()
    bp = []
    for blueprint in blueprints:
        bp.append(tuple(ints(blueprint)))
    if part == 2:
      bp = bp[:3]

    bp_geodes = []
    for (index, ore_robot_cost, clay_robot_cost, obsidian_robot_ore_cost, obsidian_robot_clay_cost, geode_robot_ore_cost, geode_robot_obsidian_cost) in bp:
      #print(f"blueprint {index}")
      states = {(1,0,0): [(0,0,0,0)]}

      max_time = 24 if part == 1 else 32

      value_of_clay = clay_robot_cost
      value_of_obsidian = obsidian_robot_ore_cost + value_of_clay * obsidian_robot_clay_cost
      value_of_geode = geode_robot_ore_cost + value_of_obsidian * geode_robot_obsidian_cost
      for t in range(max_time):
        time_left = max_time - t - 1

        # Some  creative pruning - only check states that are
        # in the better half value wise - but start pruning only after reaching 2000 states.
        values = []  
        for state, mineral_mixes in states.items():
          (ore_robots, clay_robots, obsidian_robots) = state
          for minerals in mineral_mixes:
            (ore, clay, obsidian, geode) = minerals
            value_of_state = ore + value_of_clay * clay + value_of_obsidian * obsidian + value_of_geode * geode
            value_of_state += time_left * (ore * ore_robots + value_of_clay * clay_robots + value_of_obsidian * obsidian_robots)
            values.append(value_of_state)
        values.sort()
        if len(values) > 2000:
          cutoff_value = values[len(values)//2]
        else:
          cutoff_value = values[0]

        #print("iter start", index, t, sum(len(v) for v in states.values()))
        if t == max_time - 1:
          # We can still produce a machine but it doens't produce value
          break

        new_states = {}
        decisions = [1, 2, 3, 4, 0]
        if t == max_time - 2:
          decisions = [1, 0]
        elif t == max_time - 3:
          decisions = [1, 2, 4, 0]
        for state, mineral_mixes in states.items():
          for minerals in mineral_mixes:

            machine_built = 0
            for decision in decisions:
              (ore_robots,
              clay_robots,
              obsidian_robots) = state
              (ore, clay, obsidian, geode) = minerals

              value_of_state = ore + value_of_clay * clay + value_of_obsidian * obsidian + value_of_geode * geode
              value_of_state += time_left * (ore * ore_robots + value_of_clay * clay_robots + value_of_obsidian * obsidian_robots)
              if value_of_state < cutoff_value:
                continue
              
              # Order:
              # - Decide to build machine.
              # - Produce minerals.
              # - Machine is ready.

              # Only build a machine if we need have enough resources and we more of that resources per minute.
              if decision == 1:
                if ore >= geode_robot_ore_cost and obsidian >= geode_robot_obsidian_cost:
                  ore -= geode_robot_ore_cost
                  obsidian -= geode_robot_obsidian_cost

                  ore += ore_robots
                  clay += clay_robots
                  obsidian += obsidian_robots

                  machine_built += 1
                  # Note: we don't keep track of geode machines, we just calculate the number of geode 
                  # until the end of time. Partially this is why we can't combine part 1 and part 2.
                  geode += (max_time - t - 1)
                else:
                  continue
              elif decision == 2:
                if clay >= obsidian_robot_clay_cost and ore >= obsidian_robot_ore_cost and obsidian_robots < geode_robot_obsidian_cost:
                  clay -= obsidian_robot_clay_cost
                  ore -= obsidian_robot_ore_cost
                  
                  ore += ore_robots
                  clay += clay_robots
                  obsidian += obsidian_robots

                  machine_built += 1
                  obsidian_robots += 1
                else:
                  continue
              elif decision == 3 and clay_robots < obsidian_robot_clay_cost:
                if ore >= clay_robot_cost:
                  ore -= clay_robot_cost
                  
                  ore += ore_robots
                  clay += clay_robots
                  obsidian += obsidian_robots

                  machine_built += 1
                  clay_robots += 1
                else:
                  continue
              elif decision == 4:
                if ore >= ore_robot_cost and ore_robots < max(geode_robot_ore_cost, obsidian_robot_ore_cost, clay_robot_cost, ore_robot_cost):
                  ore -= ore_robot_cost

                  ore += ore_robots
                  clay += clay_robots
                  obsidian += obsidian_robots

                  machine_built += 1
                  ore_robots += 1
                else:
                  continue
              # If we can build all 4 machines no reason not to build any.
              elif decision == 0 and machine_built != 4:      
                  ore += ore_robots
                  clay += clay_robots
                  obsidian += obsidian_robots

              new_state = (ore_robots,
              clay_robots,
              obsidian_robots)
              new_minerals = (ore, clay, obsidian, geode)
                            
              if new_state not in new_states:
                new_states[new_state] = [new_minerals]
              else:
                # Reduce the number of states:
                any_strictly_better = False
                for mineral_mix in new_states[new_state]:
                  if all(a >= b for a,b in zip(mineral_mix, new_minerals)):
                    # Don't add the state if we have a state that's strictly better.
                    any_strictly_better = True
                    break
                if not any_strictly_better:
                  # Prune any states for what this is strictly better.
                  new_states[new_state] = [mineral_mix for mineral_mix in new_states[new_state] if not all(a <= b for a,b in zip(mineral_mix, new_minerals))]
                  new_states[new_state].append(new_minerals)
        states = new_states
      # Max geodes that can be produced with this blueprint
      max_geode = max(m[3] for v in states.values() for m in v)
      bp_geodes.append(max_geode)
    
    # Output: depends on part
    if part == 1:
      total_quality = 0
      for index, max_geode in enumerate(bp_geodes, start=1):
        quality_lvl = index * max_geode
        total_quality += quality_lvl
        #print(f"for blueprint {index} quality level is {quality_lvl} with {max_geode} geodes")
      return total_quality
      
    elif part == 2:
      geode_product = 1
      for index, max_geode in enumerate(bp_geodes, start=1):
        geode_product *= max_geode
        #print(f"for blueprint {index} we have {max_geode} geodes")
      return geode_product

print(solve(TEST, part=1), "should be", 33)
print(solve(INPUT, part=1))
print(solve(TEST, part=2), "should be", 62*56)  # problem desc only gives the separate values
print(solve(INPUT, part=2))