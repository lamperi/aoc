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
            nums[a] = INPUT
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

print(run(n[:], 1))
"""
print(1, run([3,9,8,9,10,9,4,9,99,-1,8], 4))
print(0, run([3,9,8,9,10,9,4,9,99,-1,8], 8))
print(1, run([3,9,7,9,10,9,4,9,99,-1,8], 4))
print(0, run([3,9,7,9,10,9,4,9,99,-1,8], 8))
print(0, run([3,3,1108,-1,8,3,4,3,99], 4))
print(1, run([3,3,1108,-1,8,3,4,3,99], 8))
print(1, run([3,3,1107,-1,8,3,4,3,99], 4))
print(0, run([3,3,1107,-1,8,3,4,3,99], 8))
print(0, run([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], 0))
print(1, run([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], 1))
print(0, run([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], 0))
print(1, run([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], 1))
"""
print(run(n[:], 5))
