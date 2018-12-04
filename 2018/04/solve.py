data = open("input.txt").read().strip()

import re
from collections import Counter

def date_diff(date1, date2):
    assert(date1[0] == date2[0])
    assert(date1[1] == date2[1])
    assert(date1[2] == date2[2])
    return (date1[3] - date2[3])*60 + date1[4] - date2[4]

def minutes(date2, date1):
    sh = date1[3]
    m = date1[4]
    while sh < date2[3]:
        for minute in range(m, 60):
            yield minute
        m = 0
    for minute in range(m, date2[4]):
        yield minute

def solve1(data):
    guard = None
    falls = None
    sleeps = Counter()
    for line in sorted(data.splitlines()):
        if "Guard" in line:
            year,month,day,hour,minute,id = map(int, re.findall('\d+', line))
            guard = id
        else:
            year,month,day,hour,minute = map(int, re.findall('\d+', line))
            if "falls" in line:
                falls = year,month,day,hour,minute
            elif "wakes" in line and falls is not None:
                d = date_diff((year,month,day,hour,minute), falls)
                sleeps[guard] += d
    
    most_slept_guard = sleeps.most_common(1)[0]
    slept_mins = Counter()
    for line in sorted(data.splitlines()):
        if "Guard" in line:
            year,month,day,hour,minute,id = map(int, re.findall('\d+', line))
            guard = id
        else:
            if guard != most_slept_guard[0]:
                continue
            year,month,day,hour,minute = map(int, re.findall('\d+', line))
            if "falls" in line:
                falls = year,month,day,hour,minute
            elif "wakes" in line and falls is not None:
                for m in minutes((year,month,day,hour,minute), falls):
                    slept_mins[m] += 1

    most_slept_minute = slept_mins.most_common(1)[0]
    return most_slept_minute[0]*most_slept_guard[0]

print(solve1("""[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
"""))

print(solve1(data))


def solve2(data):
    guard = None
    falls = None
    slept_mins_by_guard = {}
    for line in sorted(data.splitlines()):
        if "Guard" in line:
            year,month,day,hour,minute,id = map(int, re.findall('\d+', line))
            guard = id
        else:
            year,month,day,hour,minute = map(int, re.findall('\d+', line))
            if "falls" in line:
                falls = year,month,day,hour,minute
            elif "wakes" in line and falls is not None:
                c = slept_mins_by_guard.get(guard, None)
                if c is None:
                    c = slept_mins_by_guard[guard] = Counter()
                for m in minutes((year,month,day,hour,minute), falls):
                    c[m] += 1

    max_min = (None, -1)
    max_guard = None
    for guard, slept_mins in slept_mins_by_guard.items():
        most_slept_minute = slept_mins.most_common(1)[0]
        print(max_min, most_slept_minute)
        
        if most_slept_minute[1] > max_min[1]:
            max_min = most_slept_minute
            max_guard = guard
    
    return max_min[0]*max_guard

print(solve2("""[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
"""))

print(solve2(data))
