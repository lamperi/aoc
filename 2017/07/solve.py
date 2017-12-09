import sys
data = open("input.txt").read().strip()

def func(inp):
    # multiple numbers per line:
    data = []
    val = {}
    for line in inp.splitlines():
        words = line.split()
        word = words[0]
        num = int(words[1][1:-1])
        val[word] = num
        targets = [w.split(",")[0].strip() for w in words[3:]]
        data.append((num, word, targets))
    data.sort()

    all_words = set(w[1] for w in data)
    all_targets = set(a for w in data for a in w[2])
    
    return all_words- all_targets
    
print(func("""pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)"""))
print(func(data))


def func(inp):
    # multiple numbers per line:
    data = []
    val = {}
    t = {}
    for line in inp.splitlines():
        words = line.split()
        word = words[0]
        num = int(words[1][1:-1])
        val[word] = num
        targets = [w.split(",")[0].strip() for w in words[3:]]
        t[word] = targets
        data.append((num, word, targets))
    data.sort()

    sums = {}
    
    all_words = set(w[1] for w in data)
    all_targets = set(a for w in data for a in w[2])
    
    root = list(all_words- all_targets)[0]
    
    def cum_sum(targets):
        s = 0
        for word in targets:
            if word in sums:
                return sums[word]
            v = val[word] + cum_sum(t[word])
            sums[word] = v
            s += v
        return s
                
    cs = cum_sum([root])
    sums[root] = cs
    
    print(sums)
    
    def fix_sum(targets):
        if not targets:
            return None
        current_t = None
        subsums = [sums[tar] for tar in targets]
        for index in range(len(subsums)):
            good = True
            for j in range(3):
                if index != j and subsums[index] == subsums[j]:
                    good = False
            if good:
                print(index)
                v = fix_sum(t[targets[index]])
                if v is None:
                    return val[targets[index]] + subsums[1 if index != 1 else 0] - subsums[index]
                else:
                    return v
        return None
        
    ans = fix_sum(t[root])
    return ans
    
    
print(func("""pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)"""))
print(func(data))
