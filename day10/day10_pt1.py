# Day 10 pt 1 
import re

"""
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
value = 1 
sol = 0
j = 0

print("\n")

values =[1]

while len(register) > 0: 

    value = register.pop()
    values.append(value)
    # strength = cycle number x value of register 

    j += 1
    
    if j+1 in [20,60,100,140,180,220]:
        print(values)
        print("==> ", (j+1),"x", sum(values), ":", (j+1)*sum(values), len(values))

        print("\n")
        
        sol += (j+1)*sum(values)
    

print(sol)