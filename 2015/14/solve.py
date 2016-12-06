with open("input.txt") as file:
    data = file.read()
    
import re
import itertools

class Reindeer(object):    
    def __init__(self, name, speed, fly_time, rest_time):
        self.name = name
        self.speed = speed
        self.fly_time = fly_time
        self.rest_time = rest_time
        self.cycle_time = fly_time + rest_time
        self.pos = 0
    
    def step(self, t):
        mod = t % self.cycle_time
        if mod < self.fly_time:
            self.pos += self.speed

    def __str__(self):
        return "{} at {}".format(self.name, self.pos)
    
reindeer = []
pattern = r"(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds."
for rein, speed, fly_time, rest_time in re.findall(pattern, data):
    speed = int(speed)
    fly_time = int(fly_time)
    rest_time = int(rest_time)
    reindeer.append(Reindeer(rein, speed, fly_time, rest_time))
    
scores = {}
for i in xrange(2503):
    for rein in reindeer:
        rein.step(i)
    # Award points ala part 2
    lead_pos = sorted(reindeer, lambda r1,r2: r2.pos - r1.pos)[0].pos
    s = [r.name for r in reindeer if r.pos == lead_pos]
    for n in s:
        scores[n] = 1 if n not in scores else scores[n] + 1  
        
# Part 1 distances
for rein in sorted(reindeer, lambda r1,r2: r2.pos - r1.pos):
    print(rein)
    
# Part 2 results
print(scores)
