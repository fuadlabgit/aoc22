# Day 22 pt 2
import numpy as np

# enter password
# tracing a path on a strangely shaped board
# 1. map of the board . open tiles # solid walls
# 2. description of the path you must follow
#    number = numer of tiles to move
#     letter = turn clockwise(R) ounterclockwise (L)

with open("example_input.txt", "r") as file:
    input = file.read()

lines = input.split("\n")

"""
cut the full map into 6 NxN tiles, representing the faces of the cube
"""

class Map:

    def __init__(self,data):
        """
        data is list of strings
        """
        self.M = len(data[0])
        self.N = len(data)

        self.mapdata = np.full((self.M,self.N), ".")

        for j,row in enumerate(data):
            for i,x in enumerate(row):
                assert x in [".", "#"]
                self.mapdata[i,j] = x

        self.mapdata = self.mapdata.T

    def __getitem__ (self,pos):
        # flip y coordintate
        x,y = pos
        return self.mapdata[x,y]

    def __str__(self):
        return "\n".join(["".join(row) for row in self.mapdata]).strip()

    def visualize(self,turtle):
        map = self.mapdata.copy()
        map[turtle.pos[0],turtle.pos[1]] = turtle.dirc
        print("turtle pos", turtle.pos)
        mapstr = "\n".join(["".join(row) for row in map]).strip()
        print(mapstr)

N = 4 # 4 example, 50 puzzle
cubemap = lines[:3*N]

faces = {}

faces[1] =  Map([line[2*N:3*N] for line in cubemap[:N]])
faces[2] =  Map([line[:N] for line in cubemap[N:2*N]])
faces[3] =  Map([line[N:2*N] for line in cubemap[N:2*N]])
faces[4] =  Map([line[2*N:3*N] for line in cubemap[N:2*N]])
faces[5] =  Map([line[2*N:3*N] for line in cubemap[2*N:3*N]])
faces[6] =  Map([line[3*N:4*N] for line in cubemap[2*N:3*N]])


# map the faces and directions to new faces and directions
# in this rotation map
movemap = {
   1: {"^": (2,"v"), ">": (6,"<"), "v": (4,"v"), "<": (3,"v")},
   2: {"^": (1,"v"), ">": (3,">"), "v": (5,"^"), "<": (6,"^")},
   3: {"^": (1,">"), ">": (4,">"), "v": (5,">"), "<": (2,"<")},
   4: {"^": (1,"^"), ">": (6,"v"), "v": (5,"v"), "<": (3,"<")},
   5: {"^": (4,"^"), ">": (6,">"), "v": (2,"^"), "<": (3,"^")},
   6: {"^": (4,"<"), ">": (1,"<"), "v": (2,">"), "<": (5,"<")},
}

rotmap = {
  "^": { "^":   0, ">":  90, "v": 180, "<":  -90 },
  ">": { "^": -90, ">":   0, "v":  90, "<":  180 },
  "v": { "^": 180, ">": -90, "v":   0, "<":   90 },
  "<": { "^":  90, ">": 180, "v": -90, "<":    0 },
}


"""
map coordintaes
(0,N-1) ; (1,N-1) ... ; (N-1,N-1)
...
(0,1)   ; ......
(0,0)   ; (1, 0) .....; (N-1, 0)
"""

instructions = lines[-1]
# print(instructions)

"""
Iterate through the instructions
"""


class Turtle:

    def __init__(self, face_idx, maps):
        self.pos = (0, 0) # starting position
        self.dirc = ">"
        self.face_idx = face_idx
        self.maps = maps
        self.map = maps[face_idx]

        self.N = self.map.N

    def turn_left(self):
        dirc = self.dirc

        if dirc == ">":
            dirc = "^"
        elif dirc == "^":
            dirc = "<"
        elif dirc == "<":
            dirc = "v"
        elif dirc == "v":
            dirc = ">"

        self.dirc = dirc
        self.map.visualize(self)

    def turn_right(self):
        dirc = self.dirc

        if dirc == ">":
            dirc = "v"
        elif dirc == "v":
            dirc = "<"
        elif dirc == "<":
            dirc = "^"
        elif dirc == "^":
            dirc = ">"

        self.dirc = dirc
        self.map.visualize(self)

    def rotate_position(self,pos,n_times):
        N = self.N
        my_matrix = np.zeros((N,N))
        my_matrix[pos] = 1

        for i in range(n_times):
            my_matrix = np.rot90(my_matrix)

        w = np.where(my_matrix==1)
        new_pos = (w[0][0],w[1][0])

        return new_pos

    def move(self,n_steps):

        for _ in range(n_steps):

            pos = self.pos
            dirc = self.dirc
            # compute position we would move to if it turns out to be free
            if dirc == ">":
                new_pos = (pos[0], pos[1]+1)
            elif dirc == "<":
                new_pos = (pos[0], pos[1]-1)
            elif dirc == "v":
                new_pos = (pos[0]+1, pos[1])
            elif dirc == "^":
                new_pos = (pos[0]-1, pos[1])

            # check if this position is in the map
            in_bounds = True
            if new_pos[0] < 0 or new_pos[1] < 0:
                in_bounds = False
            if new_pos[0] > self.N-1 or new_pos[1] > self.N-1:
                in_bounds = False

            if in_bounds:
                # position is in the map

                if self.map[new_pos] == ".":
                    # map is not blocked
                    self.pos = new_pos
            else:
                # position is not in the map:
                # have to wrap the map and continue
                print("position" , pos)
                self.map.visualize(self)
                # read operation for this case
                new_face, new_dirc = movemap[self.face_idx][dirc]
                print("new face", new_face, "new_dirc", new_dirc)

                # rotate map accordingly
                rotation = rotmap[self.dirc][new_dirc]
                print(pos, "rotate by ", rotation)

                if rotation == 90:
                    pos = self.rotate_position(pos,3)
                elif rotation == -90:
                    pos = self.rotate_position(pos,1)
                elif rotation == 180:
                    pos = self.rotate_position(pos,2)

                print("position after rotation", pos)

                if new_dirc == ">":
                    pos = (pos[0], pos[1]+1)
                elif new_dirc == "<":
                    pos = (pos[0], pos[1]-1)
                elif new_dirc == "v":
                    pos = (pos[0]+1, pos[1])
                elif new_dirc == "^":
                    pos = (pos[0]-1, pos[1])

                print("position after moving", pos)
                # assign new map
                if pos[0] < 0:
                    pos = (self.N - 1,pos[1])
                if pos[1] < 0:
                    pos = (pos[0],self.N - 1)
                if pos[0] > self.N -1:
                    pos = (pos[0] - (self.N), pos[1])
                if pos[1] > self.N -1:
                    pos = (pos[0], pos[1] - (self.N))

                print("shift position", pos)

                new_pos = pos

                new_map = self.maps[new_face]
                if new_map[new_pos] == ".":
                    self.map = new_map
                    self.pos = new_pos
                    self.face_idx = new_face
                    self.dirc = new_dirc

                self.map.visualize(self)

        self.map.visualize(self)


starting_face = 1
turtle = Turtle(starting_face,faces)

i = 0
buffer = ""
while i < len(instructions):

        if instructions[i] == "L":
                print("\n")
                print(buffer,instructions[i])

                n_steps = int(buffer)
                turtle.move(n_steps)
                turtle.turn_left()
                buffer = ""

                # turtle.print()

        elif instructions[i] == "R":
                print("\n")
                print(buffer,instructions[i])
                n_steps = int(buffer)
                turtle.move(n_steps)
                turtle.turn_right()
                buffer = ""

                # turtle.print()
        else:
                buffer += instructions[i]
                # print("buffer",buffer)

        i+= 1

"""
process last move
"""
n_steps = 5
turtle.move(n_steps)
turtle.map.visualize(turtle)
print(turtle.pos)

"""
Find out the code by re-constructing the original positon in the map (row and column)
"""
N = turtle.map.N

tile_offsets = {
    1: (0, 2*N),
    2: (N, 0),
    3: (N, N),
    4: (N, 2*N),
    5: (2*N, 2*N),
    6: (2*N, 3*N)
}

idx = turtle.face_idx
off_x, off_y = tile_offsets[idx]

result_1 = turtle.pos[0] + off_x + 1
result_2 = turtle.pos[1] + off_y +1

"""
encode the facing of the turtle
"""

facing_dict = {
        "^": 3,
        ">": 0,
        "v": 1,
        "<": 2
}

result_3 = facing_dict[turtle.dirc]

print("PASSWORD", 1000 * result_1 + 4* result_2 + result_3)
