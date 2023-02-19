# Day 15 part 2 

# Day 15 part 1
import re 
import numpy as np 
# start 19:10

def manhattan(x,y):
    return abs(x[0]-y[0]) + abs(x[1]-y[1])


input = """
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
""".strip().split("\n")


with open("input.txt","r") as file:
    input = file.read()
input = input.strip().split("\n")



class Interval:

    def __init__(self,x,y):
        self.x = x #  min(x,y) # int(np.ceil(min(x,y)))
        self.y = y # max(x,y) # int(np.floor(max(x,y)))

        #self.x = np.clip(self.x,0,4000000)
        #self.y = np.clip(self.y,0,4000000)

    def __repr__(self):
        return "<%i,%i>" % (self.x,self.y)

    def combine(self,other):
        # combines this interval with another interval 
        # (union). returns a list of intervals 

        u = [self.x,self.y]
        v = [other.x,other.y]

        if v[0] >= u[0] and u[1] >= v[0] and u[1] <= v[1]:
            """
            case 1: 
            u[0]---u[1]
                v[0]-------v[1]
            """
            x = [Interval(u[0],v[1])]

        elif v[0] <= u[0] and v[1] <= u[1] and v[1] >= u[0]:
            """
            case 2: 
            v[0]-------v[1]
                u[0]-------u[1] 
            """
            x = [Interval(v[0],u[1])]

        elif u[0] <= v[0] and v[1] <= u[1]:
            """
            case 3:
            u[0]----------------u[1]
                v[0]-------v[1]
            """
            x = [Interval(u[0],u[1])]

        elif v[0] <= u[0] and u[1] <= v[1]:
            """    
            case 4:
            v[0]----------------v[1]
                u[0]-------u[1]
            """
            x = [Interval(v[0],v[1])]

        elif u[1] <= v[0] and u[1] >= u[0] and v[1] >= v[0]:
            """
            case 5: 
            u[0]-------u[1]
                            v[0]-------v[1]
            """
            if u[1]+1 == v[0]:
                x = [Interval(u[0],v[1])]
            else:
                x = [Interval(u[0],u[1]),Interval(v[0],v[1])]

        elif v[1] <= u[0] and v[0] <= v[1] and u[1] >= u[0]:
            """
            case 6:    
            v[0]-------v[1]
                            u[0]-------u[1]
            """
            if v[1]+1 == u[0]:
                x = [Interval(v[0],u[1])]
            else:
                x = [Interval(v[0],v[1]),Interval(u[0],u[1])]
        
        else:
            raise RuntimeError()

        # print("    combine", u,v, "-->",x)
        return x 


sensors = []
beacons = []

for line in input:
        m = re.match("Sensor at x=(.*), y=(.*): closest beacon is at x=(.*), y=(.*)",line.strip())

        s = [int(m.group(1)),int(m.group(2))] # sensor 
        b = [int(m.group(3)),int(m.group(4))] # closest beacon

        sensors.append(s)
        beacons.append(b)


def find_coords(ref_row):

    i = []

    for ii in range(len(sensors)):

        s = sensors[ii]
        b = beacons[ii]

        # modify width by distance from source in y direction
        d = abs(s[0]-b[0]) + abs(s[1]-b[1])
        w = d - abs(ref_row-s[1])
        
        if w > 0: # print("w",w)
            x_max = s[0] +w 
            x_min = s[0] -w
            if x_max > x_min:
                x_min = np.clip(x_min,0,np.inf)
                i.append(Interval(x_min,x_max))

    i = sorted(i,key=lambda a: a.x)
    # get intersection 
    

    # unify the intervals 
    done = False

    while not done:
        done = True  

        for k in i:
            for l in i: 
                if k != l:
                    c = k.combine(l)
                    if len(c) == 1:
                        
                        i.remove(l)
                        i.remove(k)
                        i.append(c[0])

                        done = False 

                        break;

            if done:
                break;


    c = 0
    for ii in i:
        c += (ii.y - ii.x) 

    return c,i

R_min = 0
R_max = 4_000_000

for y in range(2_800_000,R_max):
    ref_row = y
    c,i = find_coords(ref_row)

    if ref_row % 5000 == 0:
        print("Progress: %.2f " % (100*ref_row/R_max))
        print(ref_row,len(i),i)
    
    # print(ref_row,i)

    if len(i) > 1:
        print("y", ref_row,"c", c, "i",i)
        break;
   

# Lösung 13639962836448
