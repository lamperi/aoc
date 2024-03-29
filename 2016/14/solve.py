
import md5
import time
import re

testKey = "abc"
inputKey = "cuanljph"


def find_64th(key, extra=0):   
    start_time = time.time()
    index = 0
    buf = []
    found = []
    while True:
         index += 1
         while buf and buf[0][0] < index - 1000:
             buf = buf[1:]
    
         m = md5.new()
         m.update(key + str(index))
         newMD5 = m.hexdigest()
         for x in range(extra):
              m = md5.new()
              m.update(newMD5)
              newMD5 = m.hexdigest()
         
         pat3 = r"(.)\1\1"
         pat5 = r"(.)\1\1\1\1"
         m = re.findall(pat5, newMD5)
         if m:
             #print("Super match: {}".format(newMD5))
             new_buf = []
             for cached in buf:
                 if cached[1] == m[0]:
                     found.append(cached)
                 else:
                     new_buf.append(cached)
             buf = new_buf
             #print("Found already {}".format(len(found)))
         m = re.findall(pat3, newMD5) # three in a row
         if m:
             #print("Match: {}".format(newMD5))
             buf.append((index, m[0], newMD5))
         if len(found) >= 64:
             break
            
    #print(found)
    solution = found[63][0]
    elapsed_time = time.time() - start_time
    print("Found {} in {}s using salt = {}".format(solution, elapsed_time, key))

find_64th(testKey, 0)
find_64th(inputKey, 0)
find_64th(testKey, 2016)
find_64th(inputKey, 2016)
