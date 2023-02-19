# Day 14 pt 2

# Day 14 pt 1 
import numpy as np 

"""

------------------------
     |
     |
     |
     |
     |          o
     |         -|-
     |         /\
-----------------------
"""


input = """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
""".strip().split("\n")

with open("input.txt","r") as file:
    input = file.read()
input = input.strip().split("\n")

rock_coords = []

for line in input:
    coords = line.split(" -> ")

    line_coords = []

    for coord in coords:
        x = int(coord.split(",")[0])
        y = int(coord.split(",")[1])
        #print("next", (x,y))

        if len(line_coords) == 0:
            #print("start at ", (x,y))
            line_coords.append((x,y))
        else:
            last_coord = line_coords[-1]

            # distance vector
            u = last_coord[0]
            v = last_coord[1]

            d_a = [(x-u),(y-v)]
            #print("   d_a", d_a )
            n = 1.0*np.sqrt(d_a[0]**2+ d_a[1]**2)
            if n > 0:
                d = [(x-u)/n,(y-v)/n]
            
            d[0] = int(d[0])
            d[1] = int(d[1])

            #print("    distance", d)
            if d[0] != 0 and d[1] != 0:
                raise RuntimeError("invalid distance vector")

            k = 0 
            while (x,y) != (u,v):
                
                
                u = u+d[0]
                v = v+d[1]

                #print("old point", (u,v), "new point",((x,y)))

                line_coords.append((u,v))
                k+=1 


    for l in line_coords:
        rock_coords.append(l)

print(rock_coords)


class Cave:

    def __init__(self,rock_coords):
        self.rock_coords = rock_coords
        self.sand_coords = []

        self.x_min = min([c[0] for c in self.rock_coords])
        self.x_max = max([c[0] for c in self.rock_coords])

        self.y_min = 0
        self.y_max = max([c[1] for c in self.rock_coords])

        self.map = np.zeros((self.x_max+200,self.y_max+20))

        for c in self.rock_coords:
            #print("block", c)
            self.map[c[0],c[1]] = 1 # 1 for rock , 2 for sand 


    def source_blocked(self):
        if self.map[500,0] == 2:
            return True 
        
        return False 

    def is_blocked(self,c):

        if c[1] == self.y_max + 2:
            return True 
        
        cond = self.map[c[0],c[1] ] == 1 or self.map[c[0],c[1]] == 2
        #print("is_blocked", c, cond)
        if cond:
            return True 
        return False 

    def insert_sand(self,x=500):
        
        p = (x,0)
        rested = False 

        while not rested:
            bottom = (p[0],p[1]+1)
            # blocked at bottom?
            if self.is_blocked(bottom):
                # print("blocked at bottom")
                # blocked a bottom left?                
                bottom_left = (p[0]-1,p[1]+1)
                if self.is_blocked(bottom_left):
                    #print("blocked left")
                    # blocked at bottom right?
                    bottom_right = (p[0]+1,p[1]+1)
                    if self.is_blocked(bottom_right):
                        #print("blocked right")
                        rested = True 

                    else:
                        p = bottom_right
                        #print("move bottom right")

                else: # bottom left not blocked 
                    p = bottom_left
                    #print("move bottom left")

            else: # bottom not blocked 
                p = bottom
                #print("move bottom",p)

        self.sand_coords.append(p)
        self.map[p[0],p[1]] = 2 # 2 for sand

        if p[0] < self.x_min :
            self.x_min = p[0]

        if p[0] > self.x_max:
            self.x_max = p[0]  

    def draw(self):

        map_str =  ""
        
        j = self.y_min
        while j <= self.y_max + 2:
            i = self.x_min - 2
            
            while i <= self.x_max + 2:

                if j == self.y_max +2 :
                    map_str += "#"
                
                elif self.map[i,j] == 1: # (i,j) in self.rock_coords:
                    map_str += "#"

                elif self.map[i,j] == 2: # (i,j) in self.sand_coords: # <- problematic if a lot of sand 
                    map_str += "o"

                else:
                    map_str += "."

                i+= 1
                
            j+= 1

            map_str += "\n"

        print(map_str)

cave = Cave(rock_coords)
cave.draw()


for i in range(50000):

    try:
        cave.insert_sand()
    except:
        cave.draw()
        print("ERROR AT %i " %i )
        break 
    
    if cave.source_blocked():
        cave.draw()
        print("BLOCKED AT %i" %(1+i) )
        break

    if i %5000 == 0:
        cave.draw()
    
