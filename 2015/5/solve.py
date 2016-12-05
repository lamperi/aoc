import re

with open("input.txt") as file:
    data = file.read()

# PART 1
def is_nice(word):
    vowels = len(re.findall(r"[aeiou]", word)) > 2
    double = len(re.findall(r"(.)\1", word)) > 0
    no_bad = len(re.findall(r"ab|cd|pq|xy", word)) == 0
    return vowels and double and no_bad

print(is_nice("ugknbfddgicrmopn"))
print(is_nice("aaa"))
print(not is_nice("jchzalrnumimnmhp"))
print(not is_nice("haegwjzuvuyypxyu"))
print(not is_nice("dvszwmarrgswjxmb"))

n = 0
for word in data.splitlines():
    if is_nice(word):
        n += 1
print(n)

def is_nice2(word):
    double = len(re.findall(r"(..).*\1", word)) > 0
    repeat = len(re.findall(r"(.).\1", word)) > 0
    return double and repeat

print(is_nice2("qjhvhtzxzqqjkmpb"))
print(is_nice2("xxyxx"))
print(not is_nice2("uurcxstgmygtbstg"))
print(not is_nice2("ieodomkazucvgmuy"))

n = 0
for word in data.splitlines():
    if is_nice2(word):
        n += 1
print(n)
