import operator as op
import itertools
import copy

with open("input.txt") as file:
    data = file.read()

class Computer(object):
    
    def __init__(self, a = 0, b = 0):
        self.inst = []
        self.reg = {"a": a, "b": b}
        self.debug = False
    
    def run(self):
        self.addr = 0
        inst_max = len(self.inst)
        while 0 <= self.addr < inst_max:
            inst = self.inst[self.addr]
            method = getattr(self, inst[0])
            method(*inst[1:])
    
    def feed(self, args):
        self.inst.append(args)
    
    def hlf(self, r):
        if self.debug: print("HLF " + r)
        self.reg[r] = int(self.reg[r] / 2)
        self.addr += 1
    
    def tpl(self, r):
        if self.debug: print("TPL " + r)
        self.reg[r] = int(self.reg[r] * 3)
        self.addr += 1
        
    def inc(self, r):
        if self.debug: print("INC " + r)
        self.reg[r] += 1
        self.addr += 1
    
    def jmp(self, offset):
        if self.debug: print("JMP " + offset)
        self.addr += int(offset)
    
    def jie(self, r, offset):
        if self.debug: print("JIE " + r + " " + offset)
        if self.reg[r] % 2 == 0:
            self.addr += int(offset)
        else:
            self.addr += 1
        
    def jio(self, r, offset):
        if self.debug: print("JIO " + r + " " + offset)
        if self.reg[r] == 1:
            self.addr += int(offset)
        else:
            self.addr += 1

computer = Computer()
for line in data.splitlines():
     args = line.replace(",", "").split()
     computer.feed(args)
     
computer.run()
print("PART 1: Computer(a={}, b={})".format(computer.reg["a"], computer.reg["b"]))

computer = Computer(a=1)
for line in data.splitlines():
     args = line.replace(",", "").split()
     computer.feed(args)
computer.run()
print("PART 2: Computer(a={}, b={})".format(computer.reg["a"], computer.reg["b"]))