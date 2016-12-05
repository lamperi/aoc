import sys
data = sys.stdin.read()

def commands():
   return (d.strip() for d in data.split(","))

def update_state(state, command):
   rotate = command[0]
   walk = int(command[1:])
   if rotate == "L":
       state[0], state[1] = -state[1], state[0]
   elif rotate == "R":
       state[0], state[1] = state[1], -state[0]
   else:
       raise Exception("Unknown command")
   state[2], state[3] = state[2] + walk*state[0], state[3] + walk*state[1]
   return state

# PART 1
def part1():
   state = [0, 1, 0, 0]
   final_state = reduce(update_state, commands(), state)
   print(final_state)
   print("Distance is {}".format(abs(final_state[2]) + abs(final_state[3])))
part1()


def walk_one_by_one(state, command):
   rotate = command[0]
   walk = int(command[1:])
   if rotate == "L":
       state[0], state[1] = -state[1], state[0]
   elif rotate == "R":
       state[0], state[1] = state[1], -state[0]
   else:
       raise Exception("Unknown command")
   for steps in range(walk):
       state[2], state[3] = state[2] + state[0], state[3] + state[1]
       yield state

# PART 2
def part2():
   state = [0, 1, 0, 0]
   visited = set()
   for command in commands():
      for state in walk_one_by_one(state, command):
        pos = tuple(state[2:])
        if pos in visited:
           print("Visited twice {}, d={}".format(pos, abs(pos[0]) + abs(pos[1])))
           return
        visited.add(pos)
part2()
