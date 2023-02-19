# Day 18 part 1 

import numpy as np 

"""
lava cools, forms obsidian

compoun of lava, cooling rate 
cooling rate is based on surface area 
"""

# surface area 

input = """
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
""".strip()

with open("input.txt","r") as file:
    input = file.read()


L = 50
W = 50 
H = 50 


space_arr = np.zeros((L,W,H),dtype=int)
boxes = []

input = input.split("\n")

for line in input:
    x = int(line.split(",")[0])
    y = int(line.split(",")[1])
    z = int(line.split(",")[2])
    print(x,y,z)
    
    space_arr[x,y,z] = 1
    boxes.append((x,y,z))


n_surfaces = 0

# print(space_arr)
for box in boxes:

    n1 = space_arr[box[0] + 1 ,box[1],box[2]] # n 1
    n2 = space_arr[box[0] - 1 ,box[1],box[2]] # n 2
    n3 = space_arr[box[0]  ,box[1] + 1,box[2]] # n 3 
    n4 = space_arr[box[0]  ,box[1] - 1,box[2]] # n 4 
    n5 = space_arr[box[0] ,box[1],box[2] + 1] # n 5
    n6 = space_arr[box[0] ,box[1],box[2] - 1] # n 6 

    nn = n1 + n2 + n3 + n4 + n5 + n6 # number of nearest neighbors

    n_surface_faces = 6 - nn 
    n_surfaces += n_surface_faces


print(n_surfaces)