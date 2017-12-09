import sys
data = open("input.txt").read().strip()

def func(inp):
    reg = {}
    for line in inp.splitlines():
        words = line.split()
        
        inp = words[4]
        comp = words[5]
        val = int(words[6])
        
        inp_val = reg.get(inp, 0)
        passed = False
        if comp == ">":
            passed= inp_val > val
        elif comp == ">=":
            passed= inp_val >= val
        elif comp == "<":
            passed= inp_val < val
        elif comp == "<=":
            passed= inp_val <= val
        elif comp == "==":
            passed= inp_val == val
        elif comp == "!=":
            passed= inp_val != val
        else:
            raise Exception("Unknown comp " + comp)
        if passed:
            out = words[0]
            verb = words[1]
            update = int(words[2])
            if verb == "inc":
                reg[out] = reg.get(out, 0) + update
            elif verb == "dec":
                reg[out] = reg.get(out, 0) - update
            else:
                raise Exception("Unknown verb " + words[1])
    
    return reg, max(b for a, b in reg.items())
    
print(func("""b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10"""))
print(func(data))



def func(inp):
    reg = {}
    any_max = 0
    for line in inp.splitlines():
        words = line.split()
        
        inp = words[4]
        comp = words[5]
        val = int(words[6])
        
        inp_val = reg.get(inp, 0)
        passed = False
        if comp == ">":
            passed= inp_val > val
        elif comp == ">=":
            passed= inp_val >= val
        elif comp == "<":
            passed= inp_val < val
        elif comp == "<=":
            passed= inp_val <= val
        elif comp == "==":
            passed= inp_val == val
        elif comp == "!=":
            passed= inp_val != val
        else:
            raise Exception("Unknown comp " + comp)
        if passed:
            out = words[0]
            verb = words[1]
            update = int(words[2])
            if verb == "inc":
                reg[out] = reg.get(out, 0) + update
            elif verb == "dec":
                reg[out] = reg.get(out, 0) - update
            else:
                raise Exception("Unknown verb " + words[1])
        if reg:
            any_max = max(any_max, max(b for a, b in reg.items()))
    
    return reg, max(b for a, b in reg.items()), any_max
    
print(func("""b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10"""))
print(func(data))
