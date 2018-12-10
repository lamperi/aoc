import re
data = open("input.txt").read().strip()

example = """position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>
"""

def print_sky(objs):

    min_x = min(x for x,y in objs)
    max_x = max(x for x,y in objs)
    min_y = min(y for x,y in objs)
    max_y = max(y for x,y in objs)

    X = max_x - min_x + 1
    Y = max_y - min_y + 1
    sky = [[' ']*X for i in range(Y)]

    for pos_x, pos_y in objs:
        sky[pos_y-min_y][pos_x-min_x] = '#'
    
    for line in sky:
        print(''.join(line))

def solve1(input):
    objs = []
    for line in input.splitlines():
        pos_x, pos_y, vel_x, vel_y = map(int, re.findall(r'-?\d+', line))
        objs.append((pos_x, pos_y, vel_x, vel_y))
    t = 0
    prev_area = None
    while True:
        objs_t = [(pos_x + t*vel_x, pos_y+t*vel_y) for pos_x, pos_y, vel_x, vel_y in objs]

        min_x = min(x for x,y in objs_t)
        max_x = max(x for x,y in objs_t)
        min_y = min(y for x,y in objs_t)
        max_y = max(y for x,y in objs_t)
        area = (abs(min_x-max_x)*abs(min_y-max_y))

        if prev_area is None:
            prev_area = area
        elif prev_area > area:
            prev_area = area
        else:
            t -= 1
            objs_t = [(pos_x + t*vel_x, pos_y+t*vel_y) for pos_x, pos_y, vel_x, vel_y in objs]
            print_sky(objs_t)
            return t
        t += 1


print(solve1(example))
print(solve1(data))