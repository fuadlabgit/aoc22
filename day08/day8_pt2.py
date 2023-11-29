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

score = np.ones_like(map)

M,N = map.shape

not_visible = 0 

for i in range(M):
    for j in range(N):

        # is on edge?
        is_edge = False 
        if j == N-1 or i == M-1:
            is_edge = True  

        ref_val = map[i,j]

        # not on edge
        # left 
        v_l = True 
        v_r = True 
        v_t = True 
        v_b = True 

        score_l = 0
        score_r = 0
        score_u = 0
        score_d = 0

        u = i-1
        while u >= 0:
            score_l += 1
            if map[u,j] >= ref_val:
                v_l = False 
                break
            

            u -= 1

        # right 
        u = i+1
        while u < M:
            score_r += 1 
            if map[u,j] >= ref_val:
                v_r = False 
                break 
            
            u += 1

        # bottom
        v = j+1
        while v < N:
            
            score_d += 1 
            if map[i,v] >= ref_val:
                v_b = False
                break 
            
            v += 1
        
        # top 
        v = j-1
        while v >= 0:
            score_u += 1 
            if map[i,v] >= ref_val:
                v_t = False 
                break 
            
            v -= 1
        
        score[i,j] = score_d * score_u * score_l * score_r
        
# print(visible)
print(score)


print(np.max(score))