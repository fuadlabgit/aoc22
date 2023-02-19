# Day 16 pt 1

import networkx as nx 
tsp = nx.approximation.traveling_salesman_problem
import re 
import matplotlib.pyplot as plt 

input = """
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
"""

input = input.strip().split("\n")

my_graph = nx.DiGraph()
labels = {}

for line in input:
    print(line)

    match = re.match("Valve (.*) has flow rate=(.*);",line)
    name = match.group(1)
    rate = match.group(2)
    
    str_conn = [s.replace(",","") for s in line.split("; ")[1].split(" ")[4:]]
    connections = str_conn

    print(name,rate,connections)
    my_graph.add_node(name,name=name,rate=rate)
    labels[name] = "%s : %s" % (name,rate)
    
    for c in connections:
        my_graph.add_edge(name,c)



nx.draw(my_graph,labels=labels)
plt.show()


class MyTree:

    def __init__(self,G):
        self.G =  G 

    def find_possibilities(self,node,time,pressure,current_path):
        """
        computes a tree with possibilities 
        given current time and pressure 
        """

        nn = self.G.neighbors(node) # get neighbors of this node 
        deeper_path = []

        for n in nn:
            p = find_possibilities(n,time+1,pressur)
            deeper_path.append(p)
        
        




