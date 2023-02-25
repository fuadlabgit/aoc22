# Day 23 part 1 
from aoc_map import Map 

"""
unstable diffusion
magma flows 
seed plant 
"""

input = """..............
..............
.......#......
.....###.#....
...#...#.#....
....#...##....
...#.###......
...##.#.##....
....#..#......
..............
..............
.............."""


input = """.....
..##.
..#..
.....
..##.
...."""

# elves # 
# empty ground . 

input = input.split("\n")



class Elve:

    instances = [] 

    def __init__(self,x,y,map,pmap):

        # Elve's coordinates
        self.x = x 
        self.y = y 

        self.map = map   # actual map 
        self.pmap = pmap # proposed positions map 

        # Proposed coordinates 
        self.px = None # proposed x
        self.py = None # proposed y 
        self.pd = None # proposed direction from current position

        self.__class__.instances.append(self)
    
    def check_all(self):
        n  = self.map.n(self.x,self.y)
        ne = self.map.ne(self.x,self.y)
        nw = self.map.nw(self.x,self.y)
        s  = self.map.s(self.x,self.y)
        se = self.map.se(self.x,self.y)
        sw = self.map.sw(self.x,self.y)
        e  = self.map.e(self.x,self.y)
        w  = self.map.w(self.x,self.y)

        if any([li == "#" for li in [n,ne,nw,s,se,sw,e,w]]):
            return False # at least one neighboring field is occupied
        
        return True # all neighboring fields unoccupied
        
    def check_north(self):
        n  = self.map.n(self.x,self.y)
        ne = self.map.ne(self.x,self.y)
        nw = self.map.nw(self.x,self.y)
        
        success = False 
        if n != "#" and ne != "#" and nw != "#":  # move north 
            if n is None or ne is None or nw is None:
                return True 
            self.px = self.x 
            self.py = self.y - 1 
            self.pd = "N"
            success = True 
        return success
    
    def check_south(self):
        s  = self.map.s(self.x,self.y)
        se = self.map.se(self.x,self.y)
        sw = self.map.sw(self.x,self.y)
        success = False 

        if s != "#" and se != "#" and sw != "#": # move south
            if s is None or se is None or sw is None:
                return True 
            self.px = self.x 
            self.py = self.y + 1 
            self.pd = "S"
            success = True 

        return success

    def check_east(self):
        e  = self.map.e(self.x,self.y)
        ne  = self.map.ne(self.x,self.y)
        se  = self.map.se(self.x,self.y)
        success = False 

        if e != "#" and ne != "#" and se != "#": # move east 
            if e is None or ne is None or ne is None:
                return True 

            self.px = self.x +1 
            self.py = self.y 
            self.pd = "E"
            success = True 
        return success

    def check_west(self):
        w  = self.map.w(self.x,self.y)
        nw  = self.map.nw(self.x,self.y)
        sw  = self.map.sw(self.x,self.y)
        success = False 

        print("   check west",w,nw,sw)
        if w != "#" and nw != "#" and sw != "#": # move west
            if w is None or nw is None or sw is None:
                return True 
            self.px = self.x -1 
            self.py = self.y 
            self.pd = "W"
            success =True 

        return success

    def propose_position(self,shift_idx):
        # 
        self.px = None 
        self.py = None
        self.pd = None 

        # look left, right up down ,... and propose a new position where to move
        w  = self.map.w(self.x,self.y)
        checks = [self.check_north,self.check_south,self.check_west,self.check_east]
        
        i = 0
        success = False 
        while not success and i < 4:
            f = checks[(i+shift_idx)%4]
            print(self,f)
            success = f()
            i+= 1 
        # print("---")

        if success and self.px is not None and self.py is not None: # self.pd is not None 
            print(self,"propose to move",self.px,",",self.py)
            self.move_pmap_pos(self.x,self.y,self.px,self.py)
    
    def move_pmap_pos(self,old_x,old_y,new_x,new_y):
        
        # print("move", old_x, old_y, new_x, new_y)

        old_elve_list = self.pmap.get_coord(old_x,old_y)
        old_elve_list.remove(self)

        new_elve_list = self.pmap.get_coord(new_x,new_y)
        new_elve_list.append(self)

        self.pmap.set_coord(old_x,old_y,old_elve_list)
        self.pmap.set_coord(new_x,new_y,new_elve_list)

    def rethink_proposal(self): 
        # re-think if proposal for new position is still ok 

        px = self.px 
        py = self.py 

        blacklist = [] 

        if px is not None and py is not None: # wants to move?
            # print("px,py",px,py)
            elve_list = self.pmap.get_coord(px,py)
            if len(elve_list) > 1:
                # overlapping elves 
                for e in elve_list: # move all back except the first
                    blacklist.append(e)
        
        return blacklist 

    def move(self):
        # move the elve 
        if self.px is not None and self.py is not None:
            
            self.x = self.px 
            self.y = self.py 
            self.pd = None 

            self.move_pmap_pos(self.x,self.y,self.px,self.py)

    def __repr__(self):
        return "<%i,%i>" % (self.x,self.y)


# create map 
map = Map(input)
map.print()

pmap = Map(input)


# create elves for the map 
for i in range(map.max_x+1):
    for j in range(map.max_y+1):

        if map.get_coord(i,j) == "#":
            new_elve = Elve(i,j,map,pmap) # store occupation here
            pmap.set_coord(i,j,[new_elve]) # store list of elves who are at, or want to move to (i,j) here 
        else:
            pmap.set_coord(i,j,[])

pmap.print()

elves = Elve.instances
print(elves)
print(len(elves))


shift_idx = 0

for kk in range(4):

    # first step: propose move 
    old_pos = [(e.x,e.y) for e in elves]

    for e in elves:
        e.propose_position(shift_idx)
        print("---------\n")

    # re-think proposals 
    blacklist = []
    for e in elves:
        blacklist += e.rethink_proposal() # append non-fitting elves to blacklist 

    # move back elves in blacklist 
    for e in blacklist:
        if e.px is not None and e.py is not None:
            print("   ....move back",e.px,e.py, "-> ", e.x,e.y)
            e.move_pmap_pos(e.px,e.py,e.x,e.y) # move back to original position
            e.px = None 
            e.py = None 
            e.pd = None # reset elve's proposal to None

    # second step: actualy move 
    for e in elves:
        e.move()

    # update map 
    for i in range(pmap.max_x+1):
        for j in range(pmap.max_y+1):
            elve_list = pmap.get_coord(i,j)
            if len(elve_list) > 0:
                map.set_coord(i,j,"#")
            else:
                map.set_coord(i,j,".")
    
    map.print()

    # shift checks index 
    shift_idx += 1