data = open("input.txt").read()
import string

example = r"""/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   
"""

def solve(input, first_dead=False):
    maze = input.splitlines()
    carts = []
    for y, line in enumerate(maze):
        for x, c in enumerate(line):
            if c == '<' or c == '>' or c == '^' or c == 'v':
                if c == '<':
                    dir = (-1, 0)
                elif c == '>':
                    dir = (1, 0)
                elif c == 'v':
                    dir = (0, 1)
                elif c == '^':
                    dir = (0, -1)
                carts.append((x,y,dir,0,string.ascii_lowercase[len(carts)]))

    maze = [line.replace('<','-').replace('>','-').replace('^','|').replace('v','|') for line in maze]

    t = 0
    pos = set()
    for cart in carts:
        pos.add((cart[0], cart[1]))
    while True:
        t+= 1
        new_carts = []
        carts = sorted(carts, key=lambda x:x[1])
        alive = 0
        for cart_index, cart in enumerate(carts):
            x,y,(dx, dy),turns,cid = cart
            if abs(dx)+abs(dy) == 0:
                continue
            alive += 1
            pos.remove((x,y))

            nx, ny = x+dx, y+dy
            
            nc = maze[ny][nx]
            #if cid == 'o' and t > 900:
            #    print(maze[0])
            #    print(t,nc,nx,ny,cart)

            if nc == '-':
                assert dy == 0
            elif nc == '|':
                assert dx == 0
            elif nc == '\\' or nc == '/':
                dx, dy = turn(nc, dx, dy)
            elif nc == '+':
                if turns % 3 == 0:
                    # left
                    # 1, 0 => 0,-1
                    # 0,-1 =>-1, 0
                    #-1, 0 => 0, 1
                    # 0, 1 => 1, 0
                    dx, dy = dy, -dx
                elif turns % 3 == 1:
                    # straight
                    pass
                else:
                    # right
                    # 1, 0 => 0, 1
                    # 0,-1 => 1, 0
                    #-1, 0 => 0,-1
                    # 0, 1 =>-1, 0
                    dx, dy = -dy, dx
                turns += 1
            else:
                print("UNKNOWN", nc)
            new_carts.append((nx, ny, (dx, dy), turns, cid))
            p = (nx, ny)
            if p in pos:
                for new_index, cart in enumerate(new_carts):
                    if (cart[0],cart[1]) == p:
                        alive -= 1
                        new_carts[new_index] = (cart[0], cart[1], (0,0), cart[3], cart[4])
                
                for cart_jndex, cart in enumerate(carts):
                    if cart_jndex > cart_index and (cart[0],cart[1]) == p:
                        carts[cart_jndex] = (cart[0], cart[1], (0,0), cart[3], cart[4])
                pos.remove(p)
                if first_dead:
                    return "{},{}".format(p[0],p[1])
            else:
                pos.add(p)
        carts = new_carts
        if alive == 0:
            return "All ded"
        if alive == 1:
            p = [(c[0],c[1]) for c in carts if c[2] != (0,0)][0]
            return "{},{}".format(p[0],p[1])

def turn(nc, dx, dy):
    if nc == '\\':
        #  1, 0 =>  0, 1
        #  0,-1 => -1, 0
        #  0, 1 =>  1, 0
        # -1, 0 =>  0,-1
        dx, dy = dy, dx
    elif nc == '/':
        # -1, 0 => 0, 1
        #  0,-1 => 1, 0
        # 1, 0 =>  0,-1
        # 0, 1 => -1, 0
        dx, dy = -dy, -dx
    else:
        assert False
    return dx, dy


assert turn('/', 0, -1) == (1, 0)
assert turn('/', -1, 0) == (0, 1)
assert turn('/', 1, 0) == (0, -1)
assert turn('/', 0, 1) == (-1, 0)

assert turn('\\', 0, -1) == (-1, 0)
assert turn('\\', -1, 0) == (0, -1)
assert turn('\\', 1, 0) == (0, 1)
assert turn('\\', 0, 1) == (1, 0)


example2 = r"""/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/
"""

print(solve(example, True))
print(solve(data, True))
print(solve(example2))
print(solve(data))