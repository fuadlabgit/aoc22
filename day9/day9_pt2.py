
# Day 9 pt 1 

# input 

lines = """
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20""".strip().split("\n")

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
    s = "move tail %s / %s " % (tail_pos,head_pos)

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

    elif d == [1,2] or d == [2,1] or d == [2,2]:
        # top right 
        tail_pos[0] += 1
        tail_pos[1] += 1

    elif d == [-1,2] or d == [-2,1] or d == [-2,2]:
        # top left 
        tail_pos[0] -= 1
        tail_pos[1] += 1
    
    elif d == [1,-2] or d == [2,-1] or d == [2,-2]:
        # bottom right 
        tail_pos[0] += 1 
        tail_pos[1] -= 1
    
    elif d == [-1,-2] or d == [-2,-1] or d == [-2,-2]:
        # bottom left 
        tail_pos[0] -= 1 
        tail_pos[1] -= 1 

    else:
        raise RuntimeError("could not interpret head direction" + str(d))

    # print( s + " --> " +  str(tail_pos))
    return tail_pos


class Element:

    def __init__(self,pos,next):
        self.pos = pos 
        self.next = next

    def move(self,instruction):

        instruction = instruction.strip() 
        self.pos = move_head(instruction,self.pos)

        item = self

        while item.next is not None:
            item.next.pos = move_tail(item.next.pos,item.pos)
            item = item.next

# rope 
tail = Element([0,0],None)
item_8 = Element([0,0],tail)
item_7 = Element([0,0],item_8)
item_6 = Element([0,0],item_7)
item_5 = Element([0,0],item_6)
item_4 = Element([0,0],item_5)
item_3 = Element([0,0],item_4)
item_2 = Element([0,0],item_3)
item_1 = Element([0,0],item_2)
head = Element([0,0],item_1)

def print_rope():
    # print("___ ROPE ____")
    for t in [tail,item_8,item_7,item_6,item_5,item_4,item_3,item_2,item_1,head]:
        print(t.pos)
    print("____")


head_pos = [0,0]
tail_pos = [0,0]

positions = []

for line in lines:

    #print("line", line) 

    direction = line[0]
    steps = int(line.split(" ")[1])

    print("=== %s,%s """ % (direction,steps)) 

    for i in range(steps):
        head.move(direction)
        positions.append((tail.pos[0],tail.pos[1]))

        # print_rope()

print(positions)
print(len(list(set(positions))))