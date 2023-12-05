import os.path

INPUT = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(INPUT) as f:
    data = f.read()

def part1(data):
    sections = data.split("\n\n")
    
    seeds = sections[0]
    seeds = [int(x) for x in seeds.split(": ")[1].split()]
    
    mappings = []
    for mapping in sections[1:]:
        mapping_lines = mapping.splitlines()
        name = mapping_lines[0]
        inst = [[int(x) for x in line.split()] for line in mapping_lines[1:]]
        mappings.append((name, inst))
    
    locations = []
    for init_seed in seeds:
        seed_values = [init_seed]
        for mapping in mappings:
            new_seeds = []
            for seed in seed_values:
                for dest_start, source_start, length in mapping[1]:
                    if source_start <= seed < source_start + length:
                        mapped = seed - source_start + dest_start
                        new_seeds.append(mapped)
            if not new_seeds:
                new_seeds.append(seed)
            seed_values = new_seeds
        locations.extend(seed_values)
    return min(locations)

test = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""
print(part1(test))
print(part1(data))

class Interval:
    def __init__(self, start, length):
        self.start = start
        self.length = length
    
    @staticmethod
    def FromStartEnd(start, end):
        return Interval(start, end-start)
    
    @property
    def end(self):
        return self.start + self.length

    def __repr__(self):
        return f'Interval(start={self.start}, end={self.end})'

class MapInterval:
    def __init__(self, dest_start, source_start, length):
        self.dest_start = dest_start
        self.source_start = source_start
        self.length = length

    @property
    def dest(self):
        return Interval(self.dest_start, self.length)

    @property
    def source(self):
        return Interval(self.source_start, self.length)

    def map(self, interval: Interval):
        return Interval(self.dest_start + interval.start - self.source_start, interval.length)

    def __repr__(self):
        return f'MapInterval(dest={self.dest}, source={self.source})'


def disjoint(i1, i2):
    return i1.end <= i2.start or i2.end <= i1.start

def intersection(i1, i2):
    start = max(i1.start, i2.start)
    end = min(i1.end, i2.end)
    if start < end:
        return Interval.FromStartEnd(start, end)

def difference(i1, i2):
    left = right = None
    if i1.start < i2.start:
        end = min(i1.end, i2.start)
        left = Interval.FromStartEnd(i1.start, end)
    if i1.end > i2.end:
        start = max(i1.start, i2.end)
        right = Interval.FromStartEnd(start, i1.end)
    return left, right

def part2(data):
    sections = data.split("\n\n")
    
    seeds = sections[0]
    seeds = [int(x) for x in seeds.split(": ")[1].split()]
    seeds_range = []
    for i in range(0, len(seeds), 2):
        seeds_range.append(Interval(seeds[i], seeds[i+1]))
    
    mappings = []
    for mapping in sections[1:]:
        mapping_lines = mapping.splitlines()
        name = mapping_lines[0]
        inst = [MapInterval(*[int(x) for x in line.split()]) for line in mapping_lines[1:]]
        mappings.append((name, inst))
    
    locations = []
    for init_interval in seeds_range:
        intervals = [init_interval]
        for mapping in mappings:
            new_intervals = []
            for interval in intervals:
                unmapped = [interval]
                for map_interval in mapping[1]:
                    if disjoint(interval, map_interval.source):
                        continue
                    is_ = intersection(interval, map_interval.source)
                    assert is_ is not None
                    mapped_is = map_interval.map(is_)
                    new_intervals.append(mapped_is)
                    new_unmapped = []
                    for u in unmapped:
                        ld, rd = difference(u, is_)
                        if ld is not None:
                            new_unmapped.append(ld)
                        if rd is not None:
                            new_unmapped.append(rd)
                    unmapped = new_unmapped
                new_intervals.extend(unmapped)
            intervals = new_intervals
        locations.extend(intervals)
    return min(x.start for x in locations)


# Override test for part 2.
# test = """ """

print(part2(test))
print(part2(data))