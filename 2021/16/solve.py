from io import TextIOBase
import os.path
import operator
from itertools import combinations, pairwise, permutations
from functools import reduce, partial
from math import isfinite, prod
from collections import Counter, defaultdict
import re
from heapq import heappush, heappop

INPUT=os.path.join(os.path.dirname(__file__), "input.txt")
with open(INPUT) as f:
    data = f.read()

replaces=dict(line.split(" = ") for line in """
0 = 0000
1 = 0001
2 = 0010
3 = 0011
4 = 0100
5 = 0101
6 = 0110
7 = 0111
8 = 1000
9 = 1001
A = 1010
B = 1011
C = 1100
D = 1101
E = 1110
F = 1111
""".splitlines() if "=" in line)

test="""D2FE28"""

def bin_to_dec(bits):
    return int("".join(str(b) for b in bits), 2)

def read_packet(data_bits):
    v = bin_to_dec(data_bits[:3])
    t = bin_to_dec(data_bits[3:6])
    if t == 4:
        i=6
        l=[]
        while True:
            n = data_bits[i]
            l.extend(data_bits[i+1:i+5])
            i+=5
            if n == 0:
                break
        p=bin_to_dec(l)
        return (i,v,t,p)
    else:
        ii=6
        l = data_bits[ii]
        ii+=1
        if l == 0:
            packet_len = bin_to_dec(data_bits[ii:ii+15])
            ii+=15
            end_index = ii+packet_len
            child=[]
            while ii < end_index:
                (read,cv,ct,cp) = read_packet(data_bits[ii:end_index])
                ii+=read
                child.append((cv,ct,cp))
            return (ii, v, t, child)
        elif l == 1:
            num_packets = bin_to_dec(data_bits[ii:ii+11])
            ii+=11
            child=[]
            for _ in range(num_packets):
                read, cv, ct, cp = read_packet(data_bits[ii:])
                ii+=read
                child.append((cv,ct,cp))
            return (ii, v, t, child)
    assert False

def sum_versions(v,t,p):
    if t == 4:
        return v
    else:
        s = v
        for c in p:
            s += sum_versions(*c)
        return s

def read_hex_packet(data):
    data=data.strip()    
    data_bits=[]
    for c in data.strip():
        bits=replaces[c]
        for b in bits:
            data_bits.append(int(b))
    return read_packet(data_bits)[1:]

def part1(data):
    data=data.strip()    
    data_bits=[]
    for c in data.strip():
        bits=replaces[c]
        for b in bits:
            data_bits.append(int(b))
    _,v,t,p = read_packet(data_bits)
    return sum_versions(v,t,p)
    

assert(read_hex_packet("""D2FE28""") == (6, 4, 2021))
assert(read_hex_packet("""38006F45291200""") == (1, 6, [(6,4,10), (2,4,20)]))
assert(read_hex_packet("""EE00D40C823060""") == (7, 3, [(2, 4, 1), (4, 4, 2), (1, 4, 3)]))
assert(part1("""8A004A801A8002F478""") == 16)
assert(part1("""620080001611562C8802118E34""") == 12)
assert(part1("""C0015000016115A2E0802F182340""") == 23)
assert(part1("""A0016C880162017C3686B18A3D4780""") == 31)
print(part1(data))

def evaluate(_,t,p):
    if t == 4:
        return p
    elif t == 0:
        return sum(evaluate(*c) for c in p)
    elif t == 1:
        return prod(evaluate(*c) for c in p)
    elif t == 2:
        return min(evaluate(*c) for c in p)
    elif t == 3:
        return max(evaluate(*c) for c in p)
    elif t == 5:
        return 1 if evaluate(*p[0]) > evaluate(*p[1]) else 0
    elif t == 6:
        return 1 if evaluate(*p[0]) < evaluate(*p[1]) else 0
    elif t == 7:
        return 1 if evaluate(*p[0]) == evaluate(*p[1]) else 0

def part2(data):
    data=data.strip()    
    data_bits=[]
    for c in data.strip():
        bits=replaces[c]
        for b in bits:
            data_bits.append(int(b))
    _,v,t,p = read_packet(data_bits)
    return evaluate(v,t,p)

assert(part2("C200B40A82") == 3)
assert(part2("04005AC33890") == 54)
assert(part2("880086C3E88112") == 7)
assert(part2("CE00C43D881120") == 9)
assert(part2("D8005AC2A8F0") == 1)
assert(part2("F600BC2D8F") == 0)
assert(part2("9C005AC2F8F0") == 0)
assert(part2("9C0141080250320F1802104A08") == 1)
print(part2(data))

