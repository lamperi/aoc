import operator as op
import itertools
import copy

class Computer(object):
    
    def __init__(self, a = 0, b = 0, c = 0, d = 0, debug = False):
        self.inst = []
        self.reg = {"a": a, "b": b, "c": c, "d": d}
        self.debug = debug
        self.debug_tgl = False
    
    def run(self):
        self.addr = 0
        inst_max = len(self.inst)
        while 0 <= self.addr < inst_max:
            inst = self.inst[self.addr]
            method = getattr(self, inst[0])
            method(*inst[1:])
    
    def feed(self, args):
        self.inst.append(args)
    
    def cpy(self, x, y):
        if self.debug: print("CPY " + x + " " + y)
        if self.isnumber(x):
            self.reg[y] = int(x)
        else:
            self.reg[y] = self.reg[x]
        self.addr += 1
    
    def dec(self, x):
        if self.debug: print("DEC " + x)
        self.reg[x] -= 1
        self.addr += 1
        
    def inc(self, x):
        if self.debug: print("INC " + x)
        self.reg[x] += 1
        self.addr += 1
        
    def jnz(self, x, y):
        if self.debug: print("JNZ " + x + " " + y)
        val = None
        if self.isnumber(x):
            val = int(x)
        else:
            val = self.reg[x]
        if val != 0:
            if self.isnumber(y):
                self.addr += int(y)
            else:
                self.addr += self.reg[y]
        else:
            self.addr += 1

    def isnumber(self, a):
        try:
            int(a)
            return True
        except Exception as e:
            return False
            
    def tgl(self, x):
        if self.debug: print("TGL " + x)
        if self.debug_tgl: print("TGL " + x + " with a as " + str(self.reg["a"]))
        if x.isdigit():
            val = int(x)
        else:
            val = self.reg[x]
        ptr = self.addr + val
        if self.debug_tgl: print("Addr: " + str(val) + " as " + str(ptr))
        if 0 <= ptr < len(self.inst):
            inst = self.inst[ptr][0]
            if inst == "inc":
                self.inst[ptr][0] = "dec"
                if self.debug_tgl: print("inc -> dec")
            elif inst == "dec":
                self.inst[ptr][0] = "inc"
                if self.debug_tgl: print("dec -> inc")
            elif inst == "tgl":
                self.inst[ptr][0] = "inc"
                if self.debug_tgl: print("tgl -> inc")
            elif inst == "cpy":
                self.inst[ptr][0] = "jnz"
                if self.debug_tgl: print("cpy -> jnz")
            elif inst == "jnz":
                self.inst[ptr][0] = "cpy"
                if self.debug_tgl: print("jnz -> cpy")
        self.addr += 1

data="""cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a
"""

computer = Computer(a=7,debug=True)
for line in data.splitlines():
     args = line.replace(",", "").split()
     computer.feed(args)
     
computer.run()
print("TEST 1: Computer(a={}, b={}, c={}, d={})".format(computer.reg["a"], computer.reg["b"], computer.reg["c"], computer.reg["d"]))

with open("input.txt") as file:
    data = file.read()

computer = Computer(a=7)
for line in data.splitlines():
     args = line.replace(",", "").split()
     computer.feed(args)
     
computer.run()
print("PART 1: Computer(eggs=7, a={})".format(computer.reg["a"]))

for eggs in range(8, 10):
    computer = Computer(a=eggs)
    for line in data.splitlines():
         args = line.replace(",", "").split()
         computer.feed(args)
    computer.run()
    print("PART 2: Computer(eggs={}, a={})".format(eggs, computer.reg["a"]))

# Formula is:
for eggs in range(7,13):
    sol = 7722 + reduce(lambda a,b: a*b, range(1,eggs+1), 1)
    print("Format: Using formula with eggs {} = {}".format(eggs, sol))