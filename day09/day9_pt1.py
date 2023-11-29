# Day 9 pt 1 

# input 

lines = """
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2""".strip().split("\n")

with open("input.txt","r") as file:
    lines = file.readlines()


# puzzle 

def move_head(instruction,head_pos):
    # moves head 
    instruction = instruction.strip()

    if instruction == "R":
        head_pos[0] += 1
    
    elif instruction == "L":
        head_pos[0] -= 1

    elif instruction == "U":
        head_pos[1] += 1 

    elif instruction == "D": 
        head_pos[1] -= 1
    
    else:
        raise RuntimeError("could not interpret instruction")

    return head_pos

def move_tail(tail_pos,head_pos):
    # moves tail 

    d = [head_pos[0]-tail_pos[0],head_pos[1]-tail_pos[1]]
    #print(d)

    if d == [0,0] or d == [0,-1] or d == [0,1] or d == [1,0] or d == [-1,0]:
        # are on top of each other 
        pass 

    elif d == [1,1] or d == [-1,-1] or d == [-1,1] or d == [1,-1]:
        pass 

    elif d == [0,2]:
        # up
        tail_pos[1] += 1  
    
    elif d == [2,0]:
        # right 
        tail_pos[0] += 1

    elif d == [-2,0]:
        # left 
        tail_pos[0] -= 1 
    
    elif d == [0,-2]:
        # down
        tail_pos[1] -= 1 

    elif d == [1,2] or d == [2,1]:
        # top right 
        tail_pos[0] += 1
        tail_pos[1] += 1

    elif d == [-1,2] or d == [-2,1]:
        # top left 
        tail_pos[0] -= 1
        tail_pos[1] += 1
    
    elif d == [1,-2] or d == [2,-1]:
        # bottom right 
        tail_pos[0] += 1 
        tail_pos[1] -= 1
    
    elif d == [-1,-2] or d == [-2,-1]:
        # bottom left 
        tail_pos[0] -= 1 
        tail_pos[1] -= 1 

    else:
        raise RuntimeError("could not interpret head direction")

    return tail_pos

head_pos = [0,0]
tail_pos = [0,0]

positions = []

for line in lines:

    #print("line", line) 

    direction = line[0]
    steps = int(line.split(" ")[1])

    #print("direction", "steps", direction, steps)

    for i in range(steps):
        # move head 
        head_pos = move_head(direction, head_pos)
        
        # move along tail
        tail_pos = move_tail(tail_pos,head_pos)
        positions.append((tail_pos[0],tail_pos[1]))

print("tail:", tail_pos)
print("head:", head_pos)

print("number of positions:", len(list(set(positions))))
