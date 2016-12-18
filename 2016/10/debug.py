with open("output.txt") as output:
    data = output.read()
    
    
produced = {}
is_producing = set()
consumed = {}
readies = 0
for line in data.splitlines():
    if ("JMSBasedValueInput" in line and "produced" in line) or "to low" in line:
        for robot in (part.split("]")[0][6:] for part in line.split("[")[2:]):
            if robot in produced:
                produced[robot] += 1
            else:
                produced[robot] = 1
    if "JMSBasedRobot" in line and "Received value" in line:
        robot = line.split(":")[3].strip()
        if robot in consumed:
            consumed[robot] += 1
        else:
            consumed[robot] = 1
    if "JMSBasedRobot" in line and "to low" in line:
        robot = line.split(":")[3].strip()
        is_producing.add(robot)
    if "JMSBasedRobot" in line and "Done" in line:
        robot = line.split(":")[3].strip()
        is_producing.remove(robot)
    if "Ready to" in line:
        readies += 1
print(produced)
print(consumed)

print([(k,v) for k,v in produced.items() if v < 2])
print([(k,v) for k,v in consumed.items() if v < 2])

print(is_producing)
print(readies)