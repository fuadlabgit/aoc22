# Day 8 pt 1
import numpy as np 


map = """
30373
25512
65332
33549
35390
""".strip().split("\n")


with open("input.txt","r") as file:
    map = file.read()
    
map = map.strip().split("\n")

map = np.array([[int(x) for x in list(m)] for m in map])

print(map)

visible = np.ones_like(map)

M,N = map.shape

not_visible = 0 

for i in range(M):
    for j in range(N):

        # is on edge?
        is_edge = False 
        if j == N-1 or i == M-1:
            visible[i,j] = 1 # just for fun 
            if_edge = True  


        ref_val = map[i,j]

        # not on edge
        # left 
        v_l = True 
        v_r = True 
        v_t = True 
        v_b = True 

        u = i-1
        while u >= 0:
            if map[u,j] >= ref_val:
                v_l = False 
            u -= 1

        # right 
        u = i+1
        while u < M:
            if map[u,j] >= ref_val:
                v_r = False 
            u += 1

        # bottom
        v = j+1
        while v < N:
            if map[i,v] >= ref_val:
                v_b = False 
            v += 1
        
        # top 
        v = j-1
        while v >= 0:
            if map[i,v] >= ref_val:
                v_t = False 
            v -= 1
        
        if not is_edge and not (v_r or v_l or v_b or v_t):
            visible[i,j] = 0
            not_visible += 1 


# print(visible)
print(np.sum(visible))
