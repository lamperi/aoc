with open("input.txt") as f:
    data = f.read().strip()

nums = [int(a) for a in data.split(",")]

def run(nums):
    pc = 0
    while True:
        #print(nums)
        if nums[pc] == 1:
            a,b = nums[nums[pc+1]], nums[nums[pc+2]]
            nums[nums[pc+3]] = a+b
        elif nums[pc] == 2:
            a,b = nums[nums[pc+1]], nums[nums[pc+2]]
            nums[nums[pc+3]] = a*b
        elif nums[pc] == 99:
            break
        pc += 4
    return nums[0]

def runp(nums, noun, verb):
    nums2=nums[:]
    nums2[1] = noun
    nums2[2] = verb
    return run(nums2)

# Example
print(run([1,9,10,3,2,3,11,0,99,30,40,50]))

# Part 1
print(runp(nums, 12, 2))

# Part 2
for noun in range(0, 100):
    for verb in range(0, 100):
        a = runp(nums, noun, verb)
        if a == 19690720:
            print(noun,verb,100*noun+verb)