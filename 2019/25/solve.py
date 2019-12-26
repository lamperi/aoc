with open("input.txt") as f:
    data = f.read().strip()
intcode = [int(a) for a in data.split(",")]

from collections import defaultdict
import sys

def run_yield(nums, get_input):
    ops = {
        1: {
            'in': 2,
            'out': 1,
            'op': lambda a, b: a+b,
        },
        2: {
            'in': 2,
            'out': 1,
            'op': lambda a, b: a*b,
        },
        3: {
            'in': 0,
            'out': 1,
            'op': lambda: next(get_input),
        },
        4: {
            'in': 1,
            'out': 0,
            'op': lambda a: OUTPUT.append(a),
            'yield': True,
        },
        5: {
            'in': 2,
            'out': 0,
            'op': lambda a, b: b if a != 0 else None,
            'jump': True,
        },
        6: {
            'in': 2,
            'out': 0,
            'op': lambda a, b: b if a == 0 else None,
            'jump': True,
        },
        7: {
            'in': 2,
            'out': 1,
            'op': lambda a,b: 1 if a < b else 0,
        },
        8: {
            'in': 2,
            'out': 1,
            'op': lambda a,b: 1 if a == b else 0,
        },
        9: {
            'in': 1,
            'out': 0,
            'op': lambda a: a,
            'rel': True,
        },
        99: {
            'in': 0,
            'out': 0,
            'op': lambda: None,
            'exit': True,
        },
    }

    pc = 0
    rel = 0
    OUTPUT = []
    # Unlimited memory
    nums = defaultdict(lambda: 0, enumerate(nums))
    while True:
        opcode = nums[pc] % 100
        if opcode == 3:
            # Have to do extra breaks for this "concurrent" exercise
            yield None
        val = int(nums[pc] / 100)
        i, j, k = int(val/100), int(val/10)%10, val%10
        if opcode in ops:
            mode = [k, j, i]
            mode_index = 0
            inputs = []
            for input_n in range(1, ops[opcode]['in']+1):
                a = nums[pc+input_n]
                if mode[mode_index] == 0:
                    a = nums[a]
                elif mode[mode_index] == 1:
                    pass
                elif mode[mode_index] == 2:
                    a = nums[a + rel]
                mode_index += 1
                inputs.append(a)
            out = ops[opcode]['op'](*inputs)
            if ops[opcode]['out'] == 1:
                a = nums[pc+1+ops[opcode]['in']]
                if mode[mode_index] == 0:
                    nums[a] = out
                elif mode[mode_index] == 1:
                    pass
                elif mode[mode_index] == 2:
                    nums[a + rel] = out
                mode_index += 1
            if ops[opcode].get('yield', False):
                yield OUTPUT[-1]
            if ops[opcode].get('rel', False):
                rel += out
            if ops[opcode].get('exit', False):
                break
            if ops[opcode].get('jump', False) and out is not None:
                pc = out
            else:
                pc += 1 + ops[opcode]['in'] + ops[opcode]['out'] 
        else:
            raise Exception('opcode={}'.format(opcode))
    return OUTPUT

# END OF INTCODE INTERPRETER
from random import choice
from itertools import combinations

def validate_rooms(rooms):
    for room, connections in rooms.items():
        for conn, other in connections.items():
            assert "rooms[{}][{}] = {}".format(room, conn, other), rooms[other][flip(conn)] == room

def direction(conn, d):
    return {
        "north": (-d, 0),
        "south": (d, 0),
        "west": (0, -d),
        "east": (0, d),
    }[conn]

def plus(a,b):
    return a[0]+b[0], a[1]+b[1]

def debug_prints(rooms):
    validate_rooms(rooms)
    s = ["digraph G {"]
    start_room = next(iter(rooms.keys()))
    pos = {start_room: (0,0)}
    for room, connections in rooms.items():
        for conn, other in connections.items():
            if other not in pos:
                pos[other] = plus(pos[room], direction(conn, 1))
            s.append("  \"{}\" -> \"{}\" [label=\"{}\"]".format(room, other, conn))
    for room, p in pos.items():
        s.append("  \"{}\" [label=\"{} ({})\"]".format(room, room, p))
    s.append("}")
    pos_to_rooms = [(v,k) for k,v in pos.items()]
    pos_to_rooms = {k: [v2 for k2,v2 in pos_to_rooms if k2==k] for k, v in pos_to_rooms}
    for same_pos_rooms in pos_to_rooms.values():
        assert len(same_pos_rooms) <= 2
        if len(same_pos_rooms) == 2:
            if "south" in rooms[same_pos_rooms[0]]:
                assert "south" not in rooms[same_pos_rooms[1]]
                same_pos_rooms.append(same_pos_rooms.pop(0))
            elif "north" in rooms[same_pos_rooms[1]]:
                assert "north" not in rooms[same_pos_rooms[0]]
                same_pos_rooms.append(same_pos_rooms.pop(0))
    print("\n".join(s))
    print_rooms(pos_to_rooms, rooms)


def print_rooms(rooms, rooms_connections):
    room_height = 8
    min_y = min(y for y,x in rooms.keys())
    min_x = min(x for y,x in rooms.keys())
    max_y = max(y for y,x in rooms.keys())
    max_x = max(x for y,x in rooms.keys())
    lines = [""] * ((1+max_y-min_y)*room_height)
    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            area_rooms = rooms.get((y,x), None)
            if area_rooms is None:
                for yy in range(room_height*(y-min_y), room_height*(y-min_y+1)):
                    lines[yy] += ("." * 22)
            else:
                top_room = area_rooms[0]
                bottom_room = area_rooms[-1]
                connecting_top_room = rooms.get(((y-1, x)), [None])[-1]
                connecting_bottom_room = rooms.get(((y+1, x)), [None])[0]
                has_top = rooms_connections[top_room].get("north", -1) == connecting_top_room
                has_bottom = rooms_connections[bottom_room].get("south", -1) == connecting_bottom_room
                has_left = "######"
                has_right = "######"
                # west connection
                west_top_connection = rooms_connections[top_room].get("west", None)
                west_bottom_connection = rooms_connections[bottom_room].get("west", None)
                west_rooms = rooms.get((y, x-1), [])
                if len(area_rooms) == 1 and len(west_rooms) == 1:
                    has_left = "##{}##".format("  " if west_rooms[0] == west_top_connection else "##")
                elif west_rooms:
                    has_top_west = west_rooms[0] == west_top_connection
                    has_bottom_west = west_rooms[-1] == west_bottom_connection
                    has_left = "{}##{}".format("  " if has_top_west else "##", "  " if has_bottom_west else "##")
                # east connection
                east_top_connection = rooms_connections[top_room].get("east", None)
                east_bottom_connection = rooms_connections[bottom_room].get("east", None)
                east_rooms = rooms.get((y, x+1), [])
                if len(area_rooms) == 1 and len(east_rooms) == 1:
                    has_right = "##{}##".format("  " if east_rooms[0] == east_top_connection else "##")
                elif east_rooms:
                    has_top_east = east_rooms[0] == east_top_connection
                    has_bottom_east = east_rooms[-1] == east_bottom_connection
                    has_right = "{}##{}".format("  " if has_top_east else "##", "  " if has_bottom_east else "##")
                room_text = [""]*(room_height-2)
                if len(area_rooms) == 1:
                    room = area_rooms[0]
                    if len(room) > 18:
                        r = room.split()
                        room_text[2] = " ".join(r[:-1])
                        room_text[3] = r[-1]
                    else:
                        room_text[2] = room
                else:
                    room = area_rooms[0]
                    if len(room) > 18:
                        r = room.split()
                        room_text[0] = " ".join(r[:-1])
                        room_text[1] = r[-1]
                    else:
                        room_text[0] = room
                    room_text[2] = "#"*20
                    room_text[3] = "#"*20
                    room = area_rooms[1]
                    if len(room) > 18:
                        r = room.split()
                        room_text[4] = " ".join(r[:-1])
                        room_text[5] = r[-1]
                    else:
                        room_text[4] = room
                        """
                    lines[room_height*(y-min_y)] += "{:#^22}".format("    " if has_top else "")
                    lines[room_height*(y-min_y)+1] += "#{: ^20}#".format(room_text[0])
                    lines[room_height*(y-min_y)+2] += "{1}{0: ^20}{2}".format(room_text[1], " " if has_left else "#", " " if has_right else "#")
                    lines[room_height*(y-min_y)+3] += "{1}{0: ^20}{2}".format(room_text[2], " " if has_left else "#", " " if has_right else "#")
                    lines[room_height*(y-min_y)+4] += "#{: ^20}#".format(room_text[3])
                    lines[room_height*(y-min_y)+5] += "#{: ^20}#".format(room_text[4])
                    lines[room_height*(y-min_y)+6] += "#{: ^20}#".format(room_text[5])
                    lines[room_height*(y-min_y)+7] += "{:#^22}".format("    " if has_bottom else "")
                    """
                lines[room_height*(y-min_y)] += "{:#^22}".format("    " if has_top else "")
                for j in range(6):
                    lines[room_height*(y-min_y)+1+j] += "{1}{0: ^20}{2}".format(room_text[j], has_left[j], has_right[j])
                lines[room_height*(y-min_y)+7] += "{:#^22}".format("    " if has_bottom else "")

    assert all(len(l) == len(lines[0]) for l in lines)
    print("\n".join(lines))

def flip(direction):
    return {
        "north": "south",
        "south": "north",
        "west": "east",
        "east": "west",
    }[direction]

def solve(intcode):
    movement = {"north", "south", "east", "west"} 
    black_list = ["molten lava", "escape pod",
    "infinite loop", "photons",
    "giant electromagnet"]
    o = []
    inv = set()
    rooms = defaultdict(dict)
    target_room = "Pressure-Sensitive Floor"
    target_check = "Security Checkpoint"
    def movement_logic():
        missing_connections = set()
        last_direction = None
        last_room = None
        #while True:
        #    print("".join(o))
        #    o.clear()
        #    yield from map(ord, "{}\n".format(input()))
        while True:
            commands = [line[2:] for line in "".join(o).splitlines() if line.startswith("- ")]
            new_rooms = [line[3:-3] for line in "".join(o).splitlines() if line.startswith("== ")]
            current_room = new_rooms[-1]
            for item in black_list:
                if item in commands:
                    commands.remove(item)
            if last_direction is not None and len(new_rooms) == 2:
                assert current_room == last_room
                rooms[last_room][last_direction] = new_rooms[0]
                missing_connections -= {(last_room, last_direction)}
                rooms[new_rooms[0]][flip(last_direction)] = last_room
            elif last_direction is not None and len(new_rooms) == 1:
                assert current_room != last_room
                rooms[last_room][last_direction] = current_room
                missing_connections -= {(last_room, last_direction)}
            if not missing_connections and current_room == target_check:
                break
            assert len(commands) > 0
            cmd = None
            if target_room in new_rooms:
                commands.remove("west")
            movement_commands = [cmd for cmd in commands if cmd in movement]
            new_movement_commands = [cmd for cmd in commands if cmd in movement and cmd not in rooms[current_room]]
            for unknown in new_movement_commands:
                missing_connections.add((current_room, unknown))
            item_commands = [cmd for cmd in commands if cmd not in movement and cmd not in inv]
            assert len(movement_commands) > 0
            if item_commands:
                cmd = choice(item_commands)
                inv.add(cmd)
                cmd = "take {}".format(cmd)
                last_room = current_room
                last_direction = None
            else:
                if new_movement_commands:
                    cmd = choice(movement_commands)
                else:
                    cmd = choice(movement_commands)

                last_room = current_room
                last_direction = cmd
                o.clear()
            yield from map(ord, cmd)
            yield ord("\n")
        debug_prints(rooms)

        def generate_drop_combinations(inv):
            #yield set(['coin', 'fuel cell', 'mutex', 'candy cane'])
            for size in range(1,8):
                yield from combinations(inv, size)
                    
        for c in generate_drop_combinations(inv):
            for item in c:
                yield from map(ord, "drop {}\n".format(item))
            o.clear()
            yield from map(ord, "west\n")
            new_rooms = [line[3:-3] for line in "".join(o).splitlines() if line.startswith("== ")]
            if target_room not in new_rooms:
                break
            for item in c:
                yield from map(ord, "take {}\n".format(item))

    for output in run_yield(intcode[:], movement_logic()):
        if output is not None:
            #sys.stdout.write(chr(output))
            o.append(chr(output))
    print("".join(c for c in o[:-1]))
    print(o[-1])
    return None

print(solve(intcode))
