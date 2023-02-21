import numpy as np 

class Map:
        def __init__(self,data_input,max_w=None ):
                
                # maximum width of the map
                if max_w is None:
                        max_w = len(data_input[0]) 
        
                self.max_w = max_w
                self.max_x = max_w-1  
                self.max_y = len(data_input)-1

                self.data = self._read_map(data_input) 
                self.default_blocked = "#"
                self.pathdata = np.full((len(data_input[0]),len(data_input)),",")
        
        def out_of_bounds(self,x,y):
                # check if coordinates are out of bounds 
                if x > self.max_x or x < 0:
                        return True 
                
                if y > self.max_y or y < 0:
                        return True 
                
                return False


        def n(self,x,y): # north 
                if y == 0:
                        return self.default_blocked
                return self.get_coord(x,y-1)

        def s(self,x,y): # south 
                if y == self.max_y:
                        return self.default_blocked
                return self.get_coord(x,y+1)
        
        def e(self,x,y): # east 
                if x == self.max_x:
                        return self.default_blocked
                return self.get_coord(x+1,y)
        
        def w(self,x,y): # west
                if y == 0:
                        return self.default_blocked
                return self.get_coord(x-1,y)
        
        def ne(self,x,y): # north-east
                if y == 0 or x == self.max_x:
                        return self.default_blocked
                return self.get_coord(x+1,y-1)
        
        def nw(self,x,y): # north-west
                if y == 0 or x == 0:
                        return self.default_blocked
                return self.get_coord(x-1,y-1)
        
        def se(self,x,y): # south-east
                if y == self.max_y or x == self.max_x:
                        return self.default_blocked
                return self.get_coord(x+1,y+1)

        def sw(self,x,y): # south-west
                if y == self.max_y or x == 0:
                        return self.default_blocked
                return self.get_coord(x-1,y+1)


        def print(self):

                if self.max_x > 500:
                        return 

                s = ""
                for i,row in enumerate(self.data):
                        for j,r in enumerate(row):
                                if self.pathdata[j][i] == ",":
                                        s+= str(r)
                                else:
                                        s+= str(self.pathdata[j][i])


                                # s+= " "
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
