import os.path
import re
import collections

FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(FILE) as f:
    INPUT = f.read()

TEST = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""

def ints(line):
    return map(int, re.findall("\d+", line))

def solve(data, number_rounds, part):
    monkey_texts = data.split("\n\n")
    monkeys = []
    for monkey in monkey_texts:
        lines = monkey.splitlines()
        items = list(ints(lines[1]))
        # Leave the parsing of the op for later
        op = lines[2].split(": ")[1]
        div_test = int(lines[3].split("Test: divisible by ")[1])
        true_throw = int(lines[4].split("If true: throw to monkey ")[1])
        false_throw = int(lines[5].split("If false: throw to monkey ")[1])
        monkeys.append({"items": items, "op": op, "div_test": div_test, "true": true_throw, "false": false_throw})
    
    # Part 2: Count the smallest number that divides all the dividers.
    # It looks like all the div tests are prime numbers so let's call
    # it "prime".
    prime = 1
    for monkey in monkeys:
        prime *= monkey["div_test"]

    inspects = collections.Counter()
    for _ in range(number_rounds):
        for mindex,monkey in enumerate(monkeys):
            for item in monkey["items"]:
                inspects[mindex] += 1
                match monkey["op"].split():
                    case "new", "=", "old", "*", "old":
                        item = item * item
                    case "new", "=", "old", "*", N:
                        item = item * int(N)
                    case "new", "=", "old", "+", "old":
                        item = item + item
                    case "new", "=", "old", "+", N:
                        item = item + int(N)
                    case other:
                        assert False, other
                if part == "part1":
                    # Part 1: Worry level is divided by two.
                    item = item//3
                elif part == "part2":
                    # Part 2: Worry level doesn't decrease - but we don't have
                    # to keep track of the actual worry levels we can operate 
                    # in (mod Prime)
                    item = item%prime
                if item % monkey["div_test"] == 0:
                    monkeys[monkey["true"]]["items"].append(item)
                else:
                    monkeys[monkey["false"]]["items"].append(item)
            monkey["items"] = []
    a, b = inspects.most_common(2)
    return a[1]*b[1]

print(solve(TEST, 20, "part1"))
print(solve(INPUT, 20, "part1"))
print(solve(TEST, 10000, "part2"))
print(solve(INPUT, 10000, "part2"))
