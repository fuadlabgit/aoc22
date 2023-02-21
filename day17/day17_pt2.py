# Day 17 part 1

import numpy as np
import matplotlib.pyplot as plt

# example input
jet = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

# my puzzle input
with open("input.txt","r") as file:
    jet = file.read()


"""
Idea of day 2 is to use a cached data array for cavedata /
we cannot save 1000000000000 rows of rocks.

--> delete the part which is full
"""

class LargeData:

    def __init__(self,cave):
        self.data = np.zeros((7,400_000))
        self.scroll_ptr = 0 # scroll pointer = vertical offset
        self.cave = cave

    def __getitem__(self,k):
        """
        retreive some of the large data entries
        """

        k = (k[0], k[1] - self.scroll_ptr)
        return self.data[k]

    def __setitem__(self,k,v):
        """
        modify some of the large data
        """

        k = (k[0], k[1] - self.scroll_ptr)
        self.data[k] = v

    def plot(self,k=0):
        plt.figure()
        plt.imshow(self.data.T,aspect="auto",interpolation="None")
        plt.axhline(self.scroll_ptr)

        plt.savefig("plots/fig_%i.png" % k )
        plt.close()

    def shrink(self):

        sp_old = self.scroll_ptr

        check_len = int(0.8*self.data.shape[1]) # < optimize runtime by theckig not all data all the end up
        N = self.cave.highest_y - sp_old
        for v in range(1,check_len): #
            if not 0 in self.data[:,N - v]:
                self.scroll_ptr = max(self.scroll_ptr, N - v)
                break

        sp = self.scroll_ptr - sp_old
        if sp > 0:

            print("shrinking point at", sp)

            N = self.data.shape[1] - sp
            remaining_data = self.data[:,sp:]
            fill_zeros = np.zeros((self.data.shape[0], sp))

            # print("remaining_data", remaining_data.shape)
            # print("fill_zeros", fill_zeros.shape)

            self.data = np.hstack((remaining_data,fill_zeros))

            # print("data shape", self.data.shape)

class Cave:
    # the whole cave

    def __init__(self,jet):
        jet_info = list(jet.strip())
        self.jet = list((jet_info))
        self.jet_iter = 0

        self.cavedata = LargeData(self) # might be too small or become too large?
        # self.cavedata[4,2] = 1  <- test

        self.highest_y = 0
        self.width = 7

    def get_direction(self):

        if self.jet_iter == len(self.jet):
            self.jet_iter = 0

        # print("   jet of gas pushes rock: %s" % self.jet[self.jet_iter])
        val =  self.jet[self.jet_iter]

        self.jet_iter += 1
        return val

    def insert_block(self,block):
        # insert new block
        x = block.x
        y = block.y

        self.highest_y = max(self.highest_y,y+1)

        for i in range(4):
            for j in range(4):

                if block.shape[i,j] == 1:
                    self.cavedata[x+i,y-j] = 1

    def is_blocked(self,block,new_x,new_y):
        # overlap rock and cave and check if it would overlap
        # return blocked, hits_floor

        collides = False
        hits_floor = False

        for i in range(4):
            for j in range(4):

                is_rock = block.shape[i,j] == 1

                if is_rock:
                    if new_y - j < 0: # hits floor
                        hits_floor = True

                    if new_x +i > 6: # hits right wall
                        collides = True

                    if new_x +i < 0: # hits left wall
                        collides = True

                    if new_x+i < 7 and self.cavedata[new_x+i,new_y-j] == 1:
                        collides = True

        return collides, hits_floor


    def print(self):

        cavestr = ""
        k = 0
        N = self.cavedata.shape[1]

        data = np.flipud(self.cavedata.T)

        for row,c in enumerate(data):

            s = "%03i |" % (N-row-1)
            for ci in c:
                if ci != 0:
                    s+= "# "
                else:
                    s+= ". "

                k+= 1

                if k > 20000:
                    print("Cave too large to print")
                    return

            s+= "|\n"
            cavestr += s

        cavestr += "    + - - - - - - -+"
        print(cavestr)



class Rock:

    instances = []

    def __init__(self,shape:int,cave):

        self.x = 2

        ydict = {
            0: 1,
            1: 3,
            2: 3,
            3: 4,
            4: 2
        }
        self.y = cave.highest_y + 2 + ydict[shape]

        self.cave = cave

        shapedict = {
            0:  np.array([[1,1,1,1],
                 [0,0,0,0],
                 [0,0,0,0],
                 [0,0,0,0]]).T,

            1:  np.array([[0,1,0,0],
                 [1,1,1,0],
                 [0,1,0,0],
                 [0,0,0,0]]).T,

            2:  np.array([[0,0,1,0],
                 [0,0,1,0],
                 [1,1,1,0],
                 [0,0,0,0]]).T,

            3:  np.array([[1,0,0,0],
                 [1,0,0,0],
                 [1,0,0,0],
                 [1,0,0,0]]).T,

            4:  np.array([[1,1,0,0],
                 [1,1,0,0],
                 [0,0,0,0],
                 [0,0,0,0]]).T,
        }
        self.shape = shapedict[shape]
        self.__class__.instances.append(self)

    def drag(self,jet_direction):
        # push left or right (if not blocked, depends on shape)

        if jet_direction == ">":
            # move right
            dx = +1

        elif jet_direction == "<":
            # move left
            dx = -1

        new_x = self.x+dx
        new_y = self.y

        # check if collides
        # print("drag -> new_x,new_y",new_x,new_y)
        collides,hits_floor = self.cave.is_blocked(self,new_x,new_y)
        # print("     collides, hits floor", collides,hits_floor)

        if not collides: #  and not hits_floor:
            self.x = new_x
            self.y = new_y


    def fall(self):
        # falling depends on shape

        new_x = self.x
        new_y = self.y -1

        # print("fall -> new_x,new_y",new_x,new_y)
        collides,hits_floor = self.cave.is_blocked(self,new_x,new_y)
        # print("    collides, hits floor", collides,hits_floor)

        if not collides and not hits_floor:
            self.x = new_x
            self.y = new_y

        ##if hits_floor and not collides:
        #    self.y -= 1

        return collides,hits_floor

    def fall_all_way(self,iters):
        # let block fall all the way down
        hits_floor = False
        collides = False
        t = 0
        while not hits_floor and not collides  and iters < max_i:
            new_rock.drag(cave.get_direction())
            collides,hits_floor = new_rock.fall()

            t+= 1
            iters += 1
            # self.cave.print()

        # print("      x,y ", self.x, self.y)
        # new_rock.drag(cave.get_direction(i))

        # brick comes to rest
        self.cave.insert_block(self)

        return iters


# 1. test large data
cave = Cave(jet)
max_i = np.inf
iters = 0

y_vals = [0]

for k in range(20_000):
    new_rock = Rock(k%5,cave)
    # print("new rock", new_rock.x,new_rock.y)
    iters = new_rock.fall_all_way(iters)
    # cave.print()

    if iters >= max_i:
        break

    #if k % 10 == 0:
    #    # cave.cavedata.plot(k)
    #    cave.cavedata.shrink()

    y_vals.append(cave.highest_y)


"""
iterating 10000... times is impossible.
however,

- we only have to find the height, not the constellation of the falling bricks
- we know there is a repeating pattern of bricks falling down

-> is there also a repeating pattern in the height of the tower?
"""

change = []
for i in range(1,len(y_vals)):
    c = (y_vals[i]- y_vals[i-1])
    change.append(c)

# find pattern
min_len = 200
max_len = 5000
found = False
for shift in range(min_len):

    for n in range(min_len,max_len):
        a = change[shift:n+shift]
        b = change[n+shift:n+n+shift]

        if a== b:
            print("FOUND")
            print(a)
            print("shift", shift, "Len(a)", len(a))
            found = True
            break

    if found:
        break

aa =  sum(a)

print("".join([str(i) for i in a]))
print(a)

print("Lengh of pattern", len(a), "total change", aa, print("shift", shift))
print("starting value", y_vals[shift])

len_pattern = len(a)
tot_change = aa
s = y_vals[shift]
t = shift
T =  1_000_000_000_000  # remaining time

iter_skip = (T-t)//len_pattern
s += tot_change * iter_skip
t += len_pattern * iter_skip

pattern = a

for i in range(T-t):
    s += pattern[i % len(pattern)]
    t+= 1

# too low 1529811924773
#         1539823008825

print(s)
