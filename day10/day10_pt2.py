import re

# Day 10 pt 2


"""
W 40 x H 6 


> ..........
..........
.......... >

X = 1 

A -> [ ... X ]
[ A ....X ]

B -> [....X ]
[ B A ... X ]

[ a a fe g  h hdf god so fi  ]  
                             ^   
"""


program = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
""".strip().split("\n")


with open("input.txt", "r") as file:
    program = file.readlines()


register = []


print("LENGTH OF PROGRAM", len(program))

for line in program:
    line = line.strip() 

    if line == "noop":
        register.insert(0,0)
        
    else:
        
        v = int(re.match("addx (.*)", line).group(1))
        # print(line,v)

        register.insert(0,0)
        register.insert(0,v)

print(register)
print("LEN(REGISTER)", len(register))

# compute solution

sol = 0
j = 0

print("\n")

pos_x = 0
pos_y = 0

sprite_center = 1 

pixels = []

while len(register) > 0:

    value = register.pop()

    pos_x = j % 40
    if pos_x % 40  == 0:
        pos_y += 1 

    if sprite_center == pos_x  or sprite_center - 1 == pos_x or sprite_center + 1 == pos_x:
        pixel = (pos_x, pos_y)
        pixels.append(pixel)
        print("    draw pixel in position", pos_x)

    sprite_center += value

    print("sprite_center", sprite_center,pos_x,pos_y)

    j+=  1

print(pixels)

import numpy as np 
screen = np.full( shape=(40,6),fill_value =" ") # "."

for p in pixels:
    screen[p[0],p[1]-1] = "#"
    
screen = screen.T 

for i in range(screen.shape[0]):
    print("".join(screen[i]))
