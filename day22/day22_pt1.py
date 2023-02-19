# Day 22 pt 1 
import numpy as np 

"""

"""

# enter password
# tracing a path on a strangely shaped board 
# 1. map of the board . open tiles # solid walls
# 2. description of the path you must follow
#    number = numer of tiles to move 
#     letter = turn clockwise(R) ounterclockwise (L)

input = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""


with open("input.txt", "r") as file:
        input = file.read()


class Map:
        def __init__(self,data_input,max_w=None ):
                self.data = self._read_map(data_input) 

                if max_w is None:
                        max_w = len(data_input[0])

                self.max_w = max_w # maximum width of the map 
                self.max_x = max_w-1
                self.max_y = len(data_input)-1

                self.pathdata = np.full((len(data_input[0]),len(data_input)),",")
        
        def print(self):

                if self.max_x > 500:
                        return 

                s = ""
                for i,row in enumerate(self.data):
                        for j,r in enumerate(row):
                                if self.pathdata[j][i] == ",":
                                        s+= r 
                                else:
                                        s+= self.pathdata[j][i]
                        s+= "\n" # "".join(row) + "\n"
                print(s)
        
        
        def get_coord(self,x,y):
                return self.data[y][x]
        
        def set_coord(self,x,y,v):
                self.data[y][x] = v 

        def _read_map(self,input):      
                # build map 
                mapdata = []

                for line in input:
                        # print("line:",line)
                        map_row = []

                        for i in range(self.max_w):
                                if i > len(line) -1:
                                        map_row.append(" ")
                                else:
                                        match line[i]:
                                                case '.':
                                                        map_row.append(".")
                                                case '#':
                                                        map_row.append("#")
                                                case ' ':
                                                        map_row.append(" ")

                        mapdata.append(map_row)
                
                return mapdata



# build instructions 
instructions = input.split("\n")[-1]

# build map 
input = input.split("\n")[:-2]
map = Map(input)

#map.set_coord(0,0,"A")
#map.set_coord(1,0,"B") < just for testing

# map.print()

class Turtle:

        def __init__(self,map):

                self.map = map # map the turtle lives in 

                self.x = 0
                self.y = 0
                self.orientation = "E"

                self.right_map = {
                        "E": "S",
                        "S": "W",
                        "W": "N",
                        "N": "E"
                }

                self.left_map = {
                        "E": "N",
                        "N": "W",
                        "W": "S", 
                        "S": "E"
                }
                self.orientation_dict = {
                        "E": ">",
                        "N": "^", 
                        "S": "v",
                        "W": "<"
                }
        def turn_right(self):
                print("turn right")
                self.orientation = self.right_map[self.orientation]
                self.update_map()
                
        def turn_left(self):
                print("turn left")
                self.orientation = self.left_map[self.orientation]
                self.update_map()

        def update_map(self):
                x = self.x 
                y = self.y 
                if self.map.get_coord(x,y) != " ":
                                self.map.pathdata[x,y] = self.orientation_dict[self.orientation]

        def move(self,n=1):
                # move n steps 
                
                k = 0 # steps moved
                
                x = self.x 
                y = self.y 

                old_x = x 
                old_y = y 
                
                while k < n:
                        
                        # print("k=",k)
                        # self.print(x,y)

                        match self.orientation:
                                case 'N':
                                        y -= 1 
                                case 'E':
                                        x += 1
                                case 'S':
                                        y += 1
                                case 'W':
                                        x -= 1
                        
                        # hit margin of map?
                        if x > self.map.max_x:
                                x = x % self.map.max_x  - 1

                        elif x < 0:
                                x = self.map.max_x 

                        elif y > self.map.max_y:
                                y = y % self.map.max_y  - 1

                        elif y < 0:
                                y = self.map.max_y
                        
                        match self.map.get_coord(x,y):
                                case '#':  
                                        # wall 
                                        # (do not move)
                                        x = old_x 
                                        y = old_y
                                        break 
                                        
                                        # k +=1
                                case '.':
                                        # normal path 
                                        old_x = x 
                                        old_y = y 

                                        k += 1 
                                case '°':
                                        # move on (no map here)
                                        pass 

                        if self.map.get_coord(x,y) != " ":
                                self.map.pathdata[x,y] = self.orientation_dict[self.orientation]

                self.x = x 
                self.y = y
                
                print("move ", n,"--->",x,y)
                # print(x,y)

        def move_to_start(self):
                reached_start = False 
                while not reached_start:
                        self.x += 1 

                        if self.map.get_coord(self.x,self.y) == ".":
                                reached_start = True 
                         
        def print(self,x=None,y=None,show=True):

                if x is None:
                        x = self.x 
                if y is None:
                        y = self.y 
                v = self.map.get_coord(x,y)
                
                self.map.set_coord(x,y,self.orientation_dict[self.orientation])

                if show:
                        self.map.print()
                self.map.set_coord(x,y,v)


turtle = Turtle(map)

# move turtle to start 
turtle.move_to_start()
turtle.print()

print("instructions", instructions)
# extract information from instructions 

i = 0
buffer = ""
while i <  len(instructions):
        

        if instructions[i] == "L":
                n_steps = int(buffer)
                turtle.move(n_steps)
                turtle.turn_left()
                buffer = "" 

                turtle.print()
                
        elif instructions[i] == "R":
                n_steps = int(buffer)
                turtle.move(n_steps)
                turtle.turn_right()
                buffer = ""

                turtle.print()
        else:
                buffer += instructions[i]
                # print("buffer",buffer)

        i+= 1 

# move last bit?
if buffer != "":
        
        last_steps = int(buffer)
        print("last step", n_steps)
        turtle.move(n_steps)
        
        turtle.print()

facing_dict = {
        "N": 3,
        "E": 0,
        "S": 1,
        "W": 2       
}

print(turtle.x+1)
print(turtle.y+1)
print(facing_dict[turtle.orientation])

pw = 1000 * (turtle.y+1) + 4 * (turtle.x+1) + facing_dict[turtle.orientation]

# 192154 too high
# 11246 too low 
# 57350
# 11246

print("solution", pw )
