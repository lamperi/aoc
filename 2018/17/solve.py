import re
data = open('input.txt').read()

def print_area(area):
    print('\n'.join(''.join(line) for line in area))

def solve(input_data, debug=False):
    x_min = x_max = 500
    y_min = 1e10
    y_max = 0
    x_ranges = []
    y_ranges = []
    for line in input_data.splitlines():
        nums = list(map(int, re.findall(r'\d+', line)))
        assert len(nums) == 3
        if line[0] == 'x':
            y_ranges.append(nums)
            x_min = min(nums[0], x_min)
            x_max = max(nums[0], x_max)
            y_min = min(nums[1], y_min)
            y_max = max(nums[2], y_max)
        else:
            x_ranges.append(nums)
            y_min = min(nums[0], y_min)
            y_max = max(nums[0], y_max)
            x_min = min(nums[1], x_min)
            x_max = max(nums[2], x_max)
    x_min -= 1
    x_max += 2
    blocks = set((y,x) for x, y1, y2 in y_ranges for y in range(y1, y2+1)) | set((y,x) for y, x1, x2 in x_ranges for x in range(x1, x2+1))
    area = [['#' if (y,x) in blocks else '.' for x in range(x_min, x_max)] for y in range(0, y_max+1)]
    area[0][500-x_min] = '+'

    water = [(0, 500)]
    while water:
        y, x = water[-1]
        # Case 0: reached bottom
        if y == y_max:
            water.pop()
        # Case 1: water flows downwards
        elif area[y+1][x-x_min] == '.':
            area[y+1][x-x_min] = '|'
            water.append((y+1, x))
        # Case 2: we are backtracking and can fill nearby
        elif area[y+1][x-x_min] == '#' or area[y+1][x-x_min] == '~':
            water.pop()
            to_rest = [(y,x)]
            free_flow = False
            for direction in (-1, 1):
                xx = x + direction
                while area[y][xx-x_min] in '.|':
                    if area[y+1][xx-x_min] == '|':
                        # Cannot go here as there is no solid ground
                        break
                    if area[y][xx-x_min] == '.':
                        area[y][xx-x_min] = '|'
                    to_rest.append((y,xx))
                    # Found new place to flow down
                    if area[y+1][xx-x_min] == '.':
                        free_flow = True
                        water.append((y,xx))
                        break
                    xx += direction
            if not free_flow:
                for yy,xx in to_rest:
                    area[yy][xx-x_min] = '~'
        # Case 2: we are backtracking and under us is flowing water
        else:
            assert area[y+1][x-x_min] == '|'
            water.pop()
    if debug:
        print_area(area)
    counted_area = sum(1 for line in area[y_min:] for tile in line if tile in '~|')
    counted_rest_area = sum(1 for line in area[y_min:] for tile in line if tile in '~')
    return counted_area, counted_rest_area

print(solve("""x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504"""))
print(solve(data))
