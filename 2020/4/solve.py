import os.path
import collections
import re
import math
INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

testdata="""ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""

def solve(data):
    passports=[]
    pp={}
    for line in data.splitlines():
        if len(line) == 0:
            passports.append(pp)
            pp={}
        parts=line.split()
        for part in parts:
            key,val = part.split(":")
            pp[key]=val
    passports.append(pp)

    s=0
    for pp in passports:
        valid = True
        for f in ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]:
            if f not in pp:
                valid = False
                break
        if valid:
            s += 1
    return s

print(2, solve(testdata))
print(solve(data))

def solve2(data):
    passports=[]
    pp={}
    for line in data.splitlines():
        if len(line) == 0:
            passports.append(pp)
            pp={}
        parts=line.split()
        for part in parts:
            key,val = part.split(":")
            pp[key]=val
    passports.append(pp)

    s=0
    y = re.compile(r"^(\d\d\d\d)$")
    h = re.compile(r"^(\d{2,3})(cm|in)$")
    c = re.compile(r"^#[0-9a-f]{6}$")
    e = re.compile(r"^(amb|blu|brn|gry|grn|hzl|oth)$")
    p = re.compile(r"^\d{9}$")
    for pp in passports:
        m = y.fullmatch(pp.get("byr", ""))
        if not m or not (1920 <= int(m[1]) <= 2002):
            continue
        m = y.fullmatch(pp.get("iyr", ""))
        if not m or not (2010 <= int(m[1]) <= 2020):
            continue
        m = y.fullmatch(pp.get("eyr", ""))
        if not m or not (2020 <= int(m[1]) <= 2030):
            continue
        m = h.fullmatch(pp.get("hgt", ""))
        if not m:
            continue
        if m[2] == "cm":
            if not (150 <= int(m[1]) <= 193):
                continue
        else:
            if not (59 <= int(m[1]) <= 76):
                continue
        if not c.fullmatch(pp.get("hcl", "")):
            continue
        if not e.fullmatch(pp.get("ecl", "")):
            continue
        if not p.fullmatch(pp.get("pid", "")):
            continue
        s += 1
    return s


print(4, solve2("""pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719"""))

print(0, solve2("""eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007"""))

print(solve2(data))
