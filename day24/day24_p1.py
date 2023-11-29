# Day 24 part 1 Blizzard Basin 
import numpy as np 
import sys


class Map:

    def __init__(self,W=5,H=5):

        self.data = np.array([set() for _ in range(W*H)]).reshape(W,H)
        # self.mapcache = {}
        self.bl = Blizz.inst

    def update(self,t):
        # reset the map 
        
        #if t in self.mapcache:
        #    self.data = self.mapcache[t]
        #    return 
        
        W,H = self.data.shape
        self.data = np.array([set() for _ in range(W*H)]).reshape(W,H)

        # update the positions
        for b in self.bl:
            p = b.update_pos(t)
            u = int(p.real)
            v = int(p.imag)

            self.data[u,v].add((b.id_numm,b.dr))
        
        #self.mapcache[t] = self.data.copy()
    
    def print(self):

        M,N = self.data.shape 

        s = "" 
        dct = { 1+0j:">", 0+1j:"v", -1+0j:"<", 0-1j:"^"}

        for i in range(N):
            for j in range(M):
                
                s+= " "
                dat = self.data[j,i] 
                if len(dat) == 0:
                    s+= "."
                elif len(dat) == 1:
                    s+= dct[next(iter(dat))[1]]
                else:
                    s+= str(len(dat))

            s+= "\n"
        
        print(s)

        #for b in self.bl:
        #    print("Blizzard at", b.pos, "pointing to", b.dr)

class Blizz:

    inst = [] 
    W = None # width and height of the basin
    H = None

    def __init__(self,pos,dr=1):

        self.pos = pos 
        self.dr = dr

        self.__class__.inst.append(self)
        self.id_numm = len(self.__class__.inst)
    
    def __repr__(self):
        return "(%s %s pointing %s)" % (self.pos.real, self.pos.imag,self.dr)

    def update_pos(self,t):
        # get position at time t 

        new_pos = self.pos + self.dr * t 
        x = int(new_pos.real) % (self.__class__.W)
        y = int(new_pos.imag) % (self.__class__.H)

        pos = x*1 + y*1j
        # print("move",self.pos, "to ", pos)
        # self.pos = pos
        return pos 

"""
(0,0j)       (M,0j)
      #.#####
      #.....#
      #>....#
      #.....#
      #...v.#
      #.....#
      #####.#
(0,Mj)       (M,Mj)
"""


lines = """#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#""".split("\n")


lines = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#""".split("\n")

with open("input.txt", "r") as file:
    lines = file.readlines()

dir_dict = {">": 1+0j, "v": 0+1j, "<": -1+0j, "^": 0-1j}

for j,line in enumerate(lines):
    line = line.strip().replace("E",".")

    for i,c in enumerate(line):
        if c not in ["#","."]:
            p = (i-1)*1. + (j-1)*1j
            Blizz(p, dir_dict[c])

W = i-1 
H = j-1

print("W,H",W,H)

start_pos = 0-1j
end_pos = (W-1) + (H)*1j # + 1j  # (W-1) + H*1j# 
print("start pos", start_pos)
print("end pos", end_pos)

Blizz.W = W 
Blizz.H = H 

MAXSTEP = 500
print("MAXSTEP", MAXSTEP) 

bl = Blizz.inst # instances of blizzards
# for b in bl:
#    print(b)

map = Map(W=W,H=H)
# map.update(t=3)

cache = {}

def dfs(maps, turt, steps):
    
    if steps >= MAXSTEP:
        print("REACHED MAXSTEP")
        return np.inf
    
    # print("dfs", turt, steps)
    # if (turt,steps) in cache:

    if (turt,steps) in cache:
        return cache[(turt,steps)] # return cache[(turt,steps)]
    
    # map.update(t=steps+1)
    # map.print()

    if turt == end_pos:
        return steps
    
    opts = [turt, turt+1, turt-1, turt+1j, turt-1j]
    valid_opts = []

    for opt in opts:
        
        u = int(opt.real)
        v = int(opt.imag)

        cond1 = u >= 0 and v >= 0
        cond2 = u <= W-1 and v <= H-1
        
        if (cond1 and cond2):
            # print(opt, "mapdata",u,v, map.data[u,v])
            # if map.data[u,v] == set():
    
            if maps[steps+1][u,v] == set():
                valid_opts.append(opt)

        if (steps <= 1 and opt == start_pos):
            valid_opts.append(opt)
        elif opt == end_pos:
            print("end pos found", opt, steps+1)
            valid_opts.append(opt)

    # print("turtle", turt , "opts",opts, "valid", valid_opts)

    if len(valid_opts) <= 0:
        return np.inf 
    
    minval = np.inf
    
    for opt in valid_opts:
        minval = min(minval, dfs(maps,opt, steps+1))

    cache[(turt,steps)] = minval 
    
    return minval


# check for map periodicity
maps = [] 
start_data = map.data.copy()

for i in range(MAXSTEP+2):
    
    map.update(t=i)
    maps.append(map.data.copy())

    if i < 7:
        print("MINUTE",i)
        map.print()

    if i % 200 == 0 and i > 0:
        print("generating map no.",i)

# map printing 
# map.update(t=17)
# map.print()
# intialize turtle at 0-1j

minval = dfs(maps, start_pos, steps=0)
print("MINVAL", minval)

# 325 too high
