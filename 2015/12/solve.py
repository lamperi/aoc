with open("input.txt") as file:
    data = file.read()

import json

data = json.loads(data)
print(data)

def walk_sum(obj):
    if isinstance(obj, int):
        return obj
    elif isinstance(obj, dict):
        return sum(walk_sum(v) for v in obj.itervalues())
    elif isinstance(obj, list):
        return sum(walk_sum(e) for e in obj)
    else:
        return 0
    
print(walk_sum(data))

def walk_red_sum(obj):
    if isinstance(obj, int):
        return obj
    elif isinstance(obj, dict):
        if "red" in obj.itervalues():
            return 0
        return sum(walk_red_sum(v) for v in obj.itervalues())
    elif isinstance(obj, list):
        return sum(walk_red_sum(e) for e in obj)
    else:
        return 0
    
print(walk_red_sum(data))