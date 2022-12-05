# Day 5, part 1 

# example input
lines = """
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
""".split("\n")


# user input
with open("input.txt","r") as file:
    lines = file.readlines()


# print("LEN",len(lines))

# create empty stacks
stacks = {
    1: [],
    2: [],
    3: [],
    4: [],
    5: [],
    6: [],
    7: [],
    8: [],
    9: [],
}

# fill stacks according to initial condition from input

for linecount,line in enumerate(lines):

    # print(line)

    if line.startswith(" 1"):
        break

    stack_info = line

    i = 0
    for j in range(9):
        my_item = stack_info[i:i+3].strip()
        # print("item",my_item)

        if my_item != "":
            stacks[j+1] = [my_item] + stacks[j+1]

        i += 4

print(stacks)

import sys 

# process movements
for idx in range(linecount+2, len(lines)):
    
    instruction = lines[idx] # 'move 1 from 2 to 1'
    
    if instruction == "\n":
        break

    # [print(str(j+1),stacks[j+1]) for j in range(9) ]
    # print("instr",instruction)

    # 6, 13, 18 
    
    idx_howmany = int(instruction.split("move ")[1].split("from")[0])
    
    idx_from = int(instruction.split("from ")[1].split("to")[0].strip()) # instruction[12]
    idx_to = int(instruction.split("to ")[1].strip()) # instruction[17]

    # print(idx_howmany,idx_from,idx_to)


    for j in range(idx_howmany):
        crate = stacks[idx_from].pop()
        stacks[idx_to].append(crate)

    # [print(str(j+1),stacks[j+1]) for j in range(9) ]
    
# print(stacks)

solution = ""

for j in range(9):

    sol = stacks[j+1]

    if len(sol) > 0:
        solution += sol[-1].replace("[","").replace("]","")
    else:
        solution += "-"

print(solution)
