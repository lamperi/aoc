data = "ckczppom"

import md5
import time

start_time = time.time()

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
         print("Part 1: {}".format(index))
     if h.startswith("000000"):
         print("Part 2: {}".format(index))
         break
                 
elapsed_time = time.time() - start_time
 
print(elapsed_time)
