
"""
e.g.
                *
                #
              #####
           ####   ####
         #####  *  #####
      #####################
       ###       ########
        ##    #########
        #


idea: start at * and walk to each surface.
"""


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

with open("input.txt","r") as file:##
    input = file.read()

boxes = []

max_x = 0
max_y = 0
max_z = 0

input = input.split("\n")

offset = 2

for line in input:

    x = int(line.split(",")[0]) + offset
    y = int(line.split(",")[1]) + offset
    z = int(line.split(",")[2]) + offset
    print(x,y,z)

    boxes.append((x,y,z))

    max_x = max(max_x,x)
    max_y = max(max_y,y)
    max_z = max(max_z,z)


bound_x  = max_x + offset
bound_y  = max_y + offset
bound_z  = max_z + offset

volume = bound_x * bound_y * bound_z

space_arr = np.zeros((bound_x, bound_y, bound_z),dtype=int)
print("volume", volume, "shape", space_arr.shape)

for box in boxes:
    space_arr[box[0],box[1],box[2]] = 1


def get_neighbors(voxel):
    """
    get coordinates of the six nearest neighboring voxels
    """

    neighbors = []

    u, v, w = space_arr.shape

    if voxel[0] < u-1:
        a =  (voxel[0] + 1, voxel[1], voxel[2])# right
        neighbors.append(a)

    if voxel[0] >= 1:
        b =  (voxel[0] - 1, voxel[1], voxel[2]) # left
        neighbors.append(b)

    if voxel[1] < v-1:
        c =  (voxel[0], voxel[1] + 1, voxel[2]) # bottom
        neighbors.append(c)

    if voxel[1] >= 1:
        d =  (voxel[0], voxel[1] - 1, voxel[2]) # top
        neighbors.append(d)

    if voxel[2] < w-1 :
        e =  (voxel[0], voxel[1], voxel[2] + 1) # forward
        neighbors.append(e)

    if voxel[2] >= 1:
        f =  (voxel[0], voxel[1], voxel[2] - 1) # backward
        neighbors.append(f)

    # print("neighbors of ", voxel, neighbors)

    return neighbors


def neighboring_boxes(voxel):
    """
    computes number of nearest neighboring boxes of a voxel
    """

    l = []
    for box in get_neighbors(voxel):
        if space_arr[box[0],box[1],box[2]] == 1:
            l.append(box)
    return l

def n_neighboring_boxes(voxel):
    """
    computes number of nearest neighboring boxes of a voxel
    """
    n =  sum([space_arr[i[0],i[1],i[2]] for i in get_neighbors(voxel)])
    return n


def get_surface_neighbors(voxel):
    """
    return a list of all neighbors of a voxel,
    if they are not filled and if they are not free-floating
    """

    surface_voxels = []

    for coord in get_neighbors(voxel):
        # print("     check", coord)
        # check its not a filled voxel and not a free-floating voxel
        if space_arr[coord[0],coord[1],coord[2]] != 1:
            #if n_neighboring_boxes(coord) > 0:
            surface_voxels.append(coord)

    return surface_voxels

def find_next_free_voxel(box):

    for coord in get_neighbors(box):
        if space_arr[coord[0],coord[1],coord[2]] != 1:
            return coord

    return None

# 1. find a starting point by 'drilling' through the structure
air_boxes = [(0,0,0),(bound_x-1,0,0),(0,bound_y-1,0),(0,0,bound_z-1),
            (0,bound_y-1,bound_z-1),(bound_x-1,bound_y-1,0), (bound_x-1,0,bound_z-1)]

new_points = air_boxes
last_len = len(air_boxes)

k = 0
while True:
    new_boxes = []

    # print("air boxes", air_boxes)
    for box in air_boxes:

        new_points = get_neighbors(box)
        # print("*new points", new_points)
        for p in new_points:
            if space_arr[p] != 1 and p not in air_boxes:
                new_boxes.append(p)

    air_boxes += new_boxes
    air_boxes = list(set(air_boxes))

    new_len = len(air_boxes)

    if new_len > last_len:
        print("found ", new_len-last_len, "new boxes","exploitation", len(air_boxes)/volume)
        last_len = new_len
        k+= 1
    else:
        break


print("no changes after", k, "iterations")
print("air boxes", len(air_boxes))

# count surface area in air boxes
s = 0

my_boxes = []
for b in air_boxes:
    for n in neighboring_boxes(b):
        s += 1
        if n not in my_boxes:
            my_boxes.append(n)

print("s", s)
print("boxes involved", len(my_boxes))
print("my_boxes", my_boxes)

# count air exposure in detected boxes
c = 0
c2 = 0
for box in my_boxes:

    for n in get_neighbors(box):
        if n in air_boxes:
            c += 1
        if space_arr[n] != 1:
            c2 += 1

print(c,c2)
