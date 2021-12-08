from io import TextIOBase
import os.path
import operator
from itertools import combinations, permutations
from functools import reduce, partial
from math import prod
from collections import Counter

INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

test="""be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""

def part1(data):
    s = 0
    for line in data.splitlines():
        patterns, output = line.split(" | ")
        patterns = patterns.split()
        output = output.split()
        s += sum(1 for p in output if len(p) in (2, 3, 4, 7))
    return s

print(part1(test))
print(part1(data))

def part2(data):
    s = 0
    for line in data.splitlines():
        patterns, output = line.split(" | ")
        patterns = patterns.split()
        output = output.split()

        map={}
        for p in patterns:
            if len(p) == 2:
                # p is 1
                map[1] = set(p)
            elif len(p) == 3:
                # p is 7
                map[7] = set(p)
            elif len(p) == 4:
                # p is 4
                map[4] = set(p)
            elif len(p) == 7:
                # p is 8:
                map[8] = set(p)
            elif len(p) == 5:
                # p is either 2, 3, 5
                if 235 not in map:
                    map[235] = set()
                map[235].add(frozenset(p))
            elif len(p) == 6:
                # p is either 0, 6, 9
                if 690 not in map:
                    map[690] = set()
                map[690].add(frozenset(p))
            else:
                raise
        assert 1 in map and 7 in map and 4 in map and 8 in map and 235 in map and 690 in map
        # Solve for the missing 6 digits
        for p in map[235]:
            if len(p&map[1]) == 2:
                map[3] = p
        for p in map[235]:
            if len(p&map[4]) == 2:
                map[2] = p
            elif len(p&map[4]) == 3:
                map[5] = p
        for p in map[690]:
            if len(p&map[1]) == 1:
                map[6] = p
            elif len(p&map[4]) == 4:
                map[9] = p
            else:
                map[0] = p
        for n in range(0,10):
            assert n in map
        # Solve the actual placement by digit by taking set differences
        a = next(iter(map[7] - map[1]))
        c = next(iter(map[8] - map[6]))
        d = next(iter(map[8] - map[0]))
        e = next(iter(map[8] - map[9]))
        b = next(iter(map[4] - map[3]))
        f = next(iter(map[1] - map[2]))
        g = next(iter(map[5] - map[4] - map[7]))
        mapping = {
            frozenset([a,b,c,e,f,g]): 0,
            frozenset([c,f]): 1,
            frozenset([a,c,d,e,g]): 2,
            frozenset([a,c,d,f,g]): 3,
            frozenset([b,c,d,f]): 4,
            frozenset([a,b,d,f,g]): 5,
            frozenset([a,b,d,e,f,g]): 6,
            frozenset([a,c,f]): 7,
            frozenset([a,b,c,d,e,f,g]): 8,
            frozenset([a,b,c,d,f,g]): 9,
        }
        i = 1
        for p in reversed(output):
            s += i*mapping[frozenset(p)]
            i *= 10
    return s

print(part2(test))
print(part2(data))

