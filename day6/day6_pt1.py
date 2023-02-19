# Day 6 

# part 1


with open("input.txt","r") as file:
    line = file.read()


def all_different(s):
    # assert len(s) == N # <- not really needed, but good to safeguard my stupidity
    return len(set(s)) == len(s)


sol = None 

# part 1 

def find_start(i):
        
    ptr = 0

    while ptr <= len(line)-i:
        if all_different(line[ptr:ptr+i]): # ,4):
            
            sol = ptr + i
            print("sol pt1",sol)
            break 

        ptr += 1 
    
find_start(4)

# part 2 

find_start(14)


"""
sol pt1 1794
sol pt2 2851
"""