import numpy as np


# part 1 

with open("input.txt","r") as file:
    lines = file.readlines()


"""
lines = [
    "A Y", 
    "B X", 
    "C Z"
]
"""


"""
shape you selected
1: rock A, X
2: paper B, Y 
3: scissors C, Z

outcome of the round 
0: lost
3: draw
6: won
"""


"""

u/v   X(R)  Y(P)  Z(S)
A(R)   3     6     0
B(P)   0     3     6
C(S)   6     0     3

"""

my_map = {
    "X": 0, 
    "A": 0,
    "Y": 1, 
    "B": 1,
    "Z": 2, 
    "C": 2
}

score_map = {
    "X": 1,
    "Y": 2,
    "Z": 3,
}

def decide(u,v):

    idx_u  = my_map[u]
    idx_v = my_map[v]

    win_lose = np.array([[3,6,0],[0,3,6],[6,0,3]])

    return win_lose[idx_u,idx_v] + score_map[v]


score = 0

for line in lines:

    u = line[0]
    # blank space = line[1]
    v = line[2]

    score += decide(u,v)


print(score)

# part 2 



"""
X(R)  Y(P)  Z(S)

u      Win    Lose   Draw
A(R)   Y      Z      X
B(P)   Z      X      Y      
C(S)   X      Y      Z

"""

strategy_map = {
    "X": 1, 
    "Y": 2, 
    "Z": 0
}

win_map = {
    "X": 0,
    "Y": 3,
    "Z": 6,
}


score = 0

for line in lines:

    u = line[0]
    s = line[2]
    idx_u  = my_map[u]

    strategy = np.array([["Y", "Z", "X"],
                         ["Z", "X", "Y"],
                         ["X", "Y", "Z"]])

    v = strategy[idx_u,strategy_map[s]]

    print("u,s,v", u, s,  v ,score_map[v] , win_map[s])

    score += score_map[v] + win_map[s]



print(score)