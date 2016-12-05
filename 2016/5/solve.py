data = "abbhdwsy"

import md5
import time

start_time = time.time()

m = md5.new()
m.update("abc3231929")
print(m.hexdigest())

index = 1
found = 5
part1 = []
part2 = ["_"]*8
while True:
     index += 1
     m = md5.new()
     m.update(data)
     m.update(str(index))
     h = m.hexdigest()
     if h.startswith("00000"):
         p2pos = int(h[5]) if h[5] in "01234567" else None
         p2key = h[6] if p2pos is not None else None
         p1key = h[5]
         print("index={}, hash={}, p1key={}, p2pos={}, p2key={}".format(index, h, p1key, p2pos, p2key))
         part1.append(p1key)
         if len(part1) == 8:
             print("part 1: " + "".join(part1))
             #break
         if p2pos is not None and part2[p2pos] == "_":
             part2[p2pos] = p2key
             if "_" not in part2:
                 print("part 2: " + "".join(part2))
                 break
        
elapsed_time = time.time() - start_time
 
print(elapsed_time)
