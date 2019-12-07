import itertools

with open("input.txt") as f:
    data = f.read().strip()

n = [int(a) for a in data.split(",")]

def run(nums, INPUT):
    pc = 0
    OUTPUT = None
    while True:
        #print(nums)
        opcode = nums[pc] % 100
        val = int(nums[pc] / 100)
        i, j, k = int(val/100), int(val/10)%10, val%10
        if opcode == 1:
            a,b = nums[pc+1], nums[pc+2]
            if k == 0:
                a = nums[a]
            if j == 0:
                b = nums[b]
            if i == 1:
                raise Exception()
            nums[nums[pc+3]] = a+b
            pc += 4
        elif opcode == 2:
            a,b = nums[pc+1], nums[pc+2]
            if k == 0:
                a = nums[a]
            if j == 0:
                b = nums[b]
            if i == 1:
                raise Exception()
            nums[nums[pc+3]] = a*b
            pc += 4
        elif opcode == 3:
            a = nums[pc+1]
            nums[a] = INPUT[0]
            INPUT = INPUT[1:]
            pc += 2
        elif opcode == 4:
            a = nums[pc+1]
            if k == 0:
                a = nums[a]
            OUTPUT = a
            pc += 2
        elif opcode == 5:
            a,b = nums[pc+1], nums[pc+2]
            if k == 0:
                a = nums[a]
            if j == 0:
                b = nums[b]
            if a != 0:
                pc = b
            else:
                pc += 3
        elif opcode == 6:
            a,b = nums[pc+1], nums[pc+2]
            if k == 0:
                a = nums[a]
            if j == 0:
                b = nums[b]
            if a == 0:
                pc = b
            else:
                pc += 3
        elif opcode == 7:
            a,b,c = nums[pc+1], nums[pc+2], nums[pc+3]
            if k == 0:
                a = nums[a]
            if j == 0:
                b = nums[b]
            if i == 1:
                raise Exception()
                #c = nums[c]
            nums[c] = 1 if a < b else 0
            pc += 4
        elif opcode == 8:
            a,b,c = nums[pc+1], nums[pc+2], nums[pc+3]
            if k == 0:
                a = nums[a]
            if j == 0:
                b = nums[b]
            if i == 1:
                raise Exception()
                #c = nums[c]
            nums[c] = 1 if a == b else 0
            pc += 4
        elif opcode == 99:
            pc += 4
            break
        else:
            raise Exception()
    return OUTPUT

def run_seq(nums, seq):
    v = 0
    for s in seq:
        v = run(nums[:], [s, v])
    return v

print(run_seq([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0], [4, 3, 2, 1, 0]))

print(max([run_seq(n[:], seq) for seq in itertools.permutations(list(range(5)))]))


def run_conn(nums, INPUT, OUTPUT):
    pc = 0
    while True:
        opcode = nums[pc] % 100
        val = int(nums[pc] / 100)
        i, j, k = int(val/100), int(val/10)%10, val%10
        if opcode == 1:
            a,b = nums[pc+1], nums[pc+2]
            if k == 0:
                a = nums[a]
            if j == 0:
                b = nums[b]
            if i == 1:
                raise Exception()
            nums[nums[pc+3]] = a+b
            pc += 4
        elif opcode == 2:
            a,b = nums[pc+1], nums[pc+2]
            if k == 0:
                a = nums[a]
            if j == 0:
                b = nums[b]
            if i == 1:
                raise Exception()
            nums[nums[pc+3]] = a*b
            pc += 4
        elif opcode == 3:
            while len(INPUT) == 0:
                yield True
                continue
            a = nums[pc+1]
            nums[a] = INPUT.pop(0)
            pc += 2
        elif opcode == 4:
            a = nums[pc+1]
            if k == 0:
                a = nums[a]
            OUTPUT.append(a)
            pc += 2
        elif opcode == 5:
            a,b = nums[pc+1], nums[pc+2]
            if k == 0:
                a = nums[a]
            if j == 0:
                b = nums[b]
            if a != 0:
                pc = b
            else:
                pc += 3
        elif opcode == 6:
            a,b = nums[pc+1], nums[pc+2]
            if k == 0:
                a = nums[a]
            if j == 0:
                b = nums[b]
            if a == 0:
                pc = b
            else:
                pc += 3
        elif opcode == 7:
            a,b,c = nums[pc+1], nums[pc+2], nums[pc+3]
            if k == 0:
                a = nums[a]
            if j == 0:
                b = nums[b]
            if i == 1:
                raise Exception()
                #c = nums[c]
            nums[c] = 1 if a < b else 0
            pc += 4
        elif opcode == 8:
            a,b,c = nums[pc+1], nums[pc+2], nums[pc+3]
            if k == 0:
                a = nums[a]
            if j == 0:
                b = nums[b]
            if i == 1:
                raise Exception()
                #c = nums[c]
            nums[c] = 1 if a == b else 0
            pc += 4
        elif opcode == 99:
            pc += 4
            break
        else:
            raise Exception()

def run_seq2(nums, seq):
    amplifiers = []
    inputs = [[a] for a in seq]
    inputs[0].append(0)
    for j, i in enumerate(inputs):
        amplifiers.append(run_conn(nums[:], i, inputs[(j+1)%len(seq)]))
    a_done = [False for a in amplifiers]
    while True:
        if sum(len(i) for i in inputs) == 0:
            return
        for i, a in enumerate(amplifiers):
            if a_done[i]:
                continue
            try:
                next(a)
            except StopIteration:
                a_done[i] = True
        if all(a_done):
            break
    return inputs[0][-1]


print(run_seq2([3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26, 27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5],[9,8,7,6,5]))
print(max([run_seq2(n[:], seq) for seq in itertools.permutations(list(range(5,10)))]))
