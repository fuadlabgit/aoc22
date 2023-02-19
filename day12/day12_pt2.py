# Day 12 pt 2 
# Day 12 pt 1 
import numpy as np 
import networkx as nx 

alphabet_map = {
    "a":0,
    "b":1,
    "c":2,
    "d":3,
    "e":4,
    "f":5,
    "g":6,
    "h":7,
    "i":8,
    "j":9,
    "k":10,
    "l":11,
    "m":12,
    "n":13,
    "o":14,
    "p":15,
    "q":16,
    "r":17,
    "s":18,
    "t":19,
    "u":20,
    "v":21,
    "w":22,
    "x":23,
    "y":24,
    "z": 25,
    "S": -1,
    "E": -2
}

map = """
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi""".strip().split("\n")

with open("input.txt","r") as file:
    map = file.read()
map = map.strip().split("\n")

k = 0
j = 0

start = []

for line in map:

    for i in line:
        if i == "S" or i == "a":
            start.append((k,j))
        if i == "E": 
            end = (k,j)

        j += 1

    j = 0    
    k+= 1 

map = [[alphabet_map[i] for i in line] for line in map]
map = np.array(map)

print("map SHAPE",map.shape)
print("start", start)
print("end", end)

map[map==-1] = 0
map[map==-2] = 25

# construct graph 
mygraph = nx.DiGraph()


def is_not_steep(u,v):
    if abs(map[v[0],v[1]] - map[u[0],u[1]]) <= 1: #  or map[v[0],v[1]] < map[u[0],u[1]]:
        return True 
    elif map[v[0],v[1]] <= map[u[0],u[1]]:
        return True 
    else:
        return False 

def steepness(u,v):
    return 1 # + abs(map[v[0],v[1]] - map[u[0],u[1]])

for x in range(map.shape[0]):
    for y in range(map.shape[1]):
        u = (x,y)
        #print("visit",u )
        # , (x-1,y), (x+1,y), (x,y-1)]:

        success = False 

        # up, left, right, down
        if y < map.shape[1]-1:
            v = (x,y+1)
            if is_not_steep(u,v):
                #print("add edge", u,v)
                mygraph.add_edge(u, v, weight=  steepness(u,v))
                success = True 

        if y > 0:
            v = (x,y-1)
            if is_not_steep(u,v):
                #print("add edge", u,v)
                mygraph.add_edge(u, v, weight= steepness(u,v))
                success = True 

        if x < map.shape[0]-1:
            v = (x+1,y)
            if is_not_steep(u,v):
                #print("add edge", u,v)
                mygraph.add_edge(u, v, weight= steepness(u,v))
                success = True 

        if x > 0:
            v = (x-1,y)
            if is_not_steep(u,v):
                #print("add edge", u,v)
                mygraph.add_edge(u, v, weight= steepness(u,v))
                success = True 

        if not success:
            nb = " , ".join([str(map[u[0],u[1]+1]),str(map[u[0]+1,u[1]]),str(map[u[0]-1,u[1]]),str(map[u[0],u[1]-1])])
            # raise RuntimeError(str(u) + " " + str(map[u[0],u[1]]) +  " neighbors "  + nb)

print(mygraph)


all_steps = []
for start_i in start: 
    
    try:
        sps = nx.all_shortest_paths(mygraph,source=start_i,target=end ,weight="weight")
        shortest_path = next(sps)

        steps = 0
        for i in range(len(shortest_path)-1):
            
            u = shortest_path[i]
            v = shortest_path[i+1]

            s = 1 # abs(map[v[0],v[1]] - map[u[0],u[1]]) + 1
            # print(u,v, "s", s )
            steps += s

        print(steps)
        all_steps.append(steps)

    except:
        pass

print("SOLUTION", min(all_steps))

