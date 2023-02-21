# Day 16 pt 1

import networkx as nx
tsp = nx.approximation.traveling_salesman_problem
import re
import matplotlib.pyplot as plt
from collections import defaultdict


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


with open("input.txt", "r") as file:
    input = file.readlines()


print(input)

my_graph = nx.DiGraph()
labels = {}

for line in input:
    print(line)

    match = re.match("Valve (.*) has flow rate=(.*);",line)
    name = match.group(1).strip()
    rate = match.group(2)

    str_conn = [s.replace(",","").strip() for s in line.split("; ")[1].split(" ")[4:]]
    connections = str_conn

    # print(name,rate,connections)
    my_graph.add_node(name,name=name,rate=rate)
    labels[name] = "%s : %s" % (name,rate)

    for c in connections:
        my_graph.add_edge(name,c)

nx.draw(my_graph,labels=labels)
# plt.show()

"""
List all connections with valves of flow rate != 0
"""
path = nx.all_pairs_shortest_path_length(my_graph)
distance = {x[0]:x[1] for x in path} # construct shortest path distances

my_names = nx.get_node_attributes(my_graph, "name")
my_rates = nx.get_node_attributes(my_graph, "rate")
flow_rate = {my_names[n]: int(my_rates[n]) for n in my_graph.nodes}

my_nodes = [node for node in my_graph.nodes if flow_rate[node] > 0 or my_names[node] =="AA"]
# non-zero nodes and node A
print("my_nodes",my_nodes)

nz_dist = defaultdict(lambda: {}) # non-zero flow valve distances

for node_i in my_nodes:
    for node_j, d in distance[node_i].items():
        if node_j != node_i and node_j in my_nodes:
            nz_dist[node_i][node_j] = d

print("Non-Zero Flow Valves distances:", nz_dist)

"""
hyper-neutrinos solution:

Use an 'intelligent brute-force' algorithm
Store the used situations in a cache
use a bitmask wether valve is open

first, find the relevant valves and put them into a bitmask
closed will be 0 , open will be 1
"""

valve_idx = {}
for i, node in enumerate(my_nodes):
    valve_idx[node] = i

print("valve index", valve_idx)

"""
Define the bfs
"""
cache = {}

def dfs(time, valve, bitmask):
    """
    perform a depth-first search

    :param time: the remaining time we have to solve the puzzle
    :param valves: tuple, valve we are at and the elephant is at
    :param bitmask: the current state of the system
    """

    # first, look up if the answer has already been computed
    # get from cache in that case
    starting_condition = (time, valve, bitmask)

    if starting_condition in cache:
        return cache[starting_condition]

    # print("starting condition", starting_condition, "not yet in cache")
    # in case the current starting position has not yet been computed,
    # ... dot it now!

    # print("inspect neighbors of ", valve, nz_dist[valve])
    maxval = 0 # maximum amount of flow we can get in this situation

    # look for the best valve to open next
    for neighbor in nz_dist[valve]:

        # print("inspect neighbor", neighbor)

        # is the current neighbor open?
        # don't consider turning this neighbor on as the maxval will not change
        bit = 1  << valve_idx[neighbor]
        if bitmask & bit:
            continue

        # time consumed to go to a valve and open it.
        # opening a valve costs one additional time step
        time_left = time - (nz_dist[valve][neighbor] + 1)

        # if we have not enough time left,
        # skip this possibility
        if time_left <= 0:
            continue

        # print("visit", neighbor, "time left", time_left)

        # update the maxval
        gain = flow_rate[neighbor] * time_left # gain from opening this valve

        # potentail gain from this move
        new_state = bitmask | bit
        new_val = gain + dfs(time_left, neighbor, new_state)

        # reached new high-score?
        maxval = max(new_val, maxval)

    # add new state to the cache
    cache[starting_condition] = maxval

    return maxval

"""
Elephant and me do the work together
Elephant opens all the valves I cannot open, i.e.
"""

useful_valves = list(valve_idx.keys())
useful_valves.remove("AA")
print("useful valves", useful_valves)

# make a bitmask for all open valves
all_valves = (1 << len(useful_valves)) -1

combined_max = 0 #

# compute the result
N = (all_valves + 1)//2
for i in range(N):

    print("progress: %.2f percent" %  (100. * (1.0*i)/N))

    my_valves = i
    elephant_valves = all_valves^i

    max_my = dfs(26,"AA", i) # I do one part
    max_elephant = dfs(26,"AA", all_valves^i) # elephant does other part
    combined_max = max(combined_max, max_my + max_elephant)

print(combined_max)
