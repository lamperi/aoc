with open("input.txt") as f:
    data = f.read()

bots = 1000
inputs = [[False] for i in range(bots)]
outputs = [[] for i in range(bots)]
maps = [[] for i in range(bots)]

for line in data.splitlines():
    if line.startswith("value"):
       p = line.split()
       val = int(p[1])    
       bot = int(p[-1])
       inputs[bot].append(val)
    elif line.startswith("bot"):
       p = line.split()
       fbot = int(p[1])
       lowtype = p[5]
       tolow = int(p[6])
       hightype = p[-2]
       tohigh = int(p[-1])
       maps[fbot].append((lowtype, tolow))
       maps[fbot].append((hightype, tohigh))

while True:
    found = False
    for bot_id, input_set in enumerate(inputs):
        if not input_set[0] and len(input_set) == 3:
            found = True
            input_set[0] = True
            low,high = sorted(input_set[1:])
            if low == 17 and high == 61:
                print("PART 1: {}".format(bot_id))
            low_target,high_target = maps[bot_id]
            if low_target[0] == "bot":
                inputs[low_target[1]].append(low)
            else:
                outputs[low_target[1]].append(low)
            if high_target[0] == "bot":
                inputs[high_target[1]].append(high)
            else:
                outputs[high_target[1]].append(high)
            #print("Bot {} gives {} to {} and {} to {}".format(bot_id, low, low_target, high, high_target))
    if not found:
        break
                
res = outputs[0][0] * outputs[1][0] * outputs[2][0]
print("PART 2: {}".format(res))
