# Day 13 part 2

# Day 13 part 1

input = """
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]""".strip().split("\n\n")
 

with open("input.txt","r") as file:
    input = file.read()   
input = input.split("\n\n")


def compare(left, right, t=0):

    #print("\t"*t , "- Compare %s vs %s" % (left, right))

    is_right_order = None 

    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            #print("\t"*(t+1) , "- Left side is smaller, so inputs are in right order")
            return True  # continue checking
        elif left == right:
            return None
        elif left > right:
            #print("\t"*(t+1) , "- Right side is smaller, so inputs are NOT in right order")
            return False # wrong order    

    elif isinstance(left, list) and isinstance(right, list):
        
        m =  len(left)-1
        n =  len(right)-1

        for i in range(max(m+1,n+1)):

            if i > m and i <= n: # left runs out first
                #print("\t"*(t+1) , "- Left side runs out -> right order")
                return True 
            elif i <= m and i > n: # right runs out first
                #print("\t"*(t+1) , "- Right side runs out -> NOT right order")
                return False 
            else:
                is_right_order = compare(left[i],right[i],t+1)
                
                if is_right_order is not None:
                    return is_right_order

        
    elif isinstance(left,list) and isinstance(right,int):
        #print("\t"*(t+1) , "- Mixed types; convert right to %s and retry comparison" % [right])
        return compare(left,[right],t+1)
    
    elif isinstance(left,int) and isinstance(right,list):
        #print("\t"*(t+1) , "- Mixed types; convert left to %s and retry comparison" % [left])
        return compare([left],right,t+1)
    

    return is_right_order


my_pairs = []

i = 1

for line in input:
    pair_left = eval(line.split("\n")[0])
    pair_right = eval(line.split("\n")[1])

    #print("== Pair %i ==" %i )
    print(pair_left,"vs. ",pair_right)
    success = compare(pair_left,pair_right)
    print("IS RIGHT ORDER?", success)

    if success:
        my_pairs.append(pair_left)
        my_pairs.append(pair_right)
    else:
        my_pairs.append(pair_right)
        my_pairs.append(pair_left)

    i+=1

    print("\n")

print("pairs",my_pairs)

# bubble sort 
k = 0
all_sorted = False 

my_pairs += [[[2]]]
my_pairs += [[[6]]]

while not all_sorted:

    all_sorted = True 
    for i in range(len(my_pairs)-1):
        a = my_pairs[i]
        b = my_pairs[i+1]

        if not compare(a,b):
            my_pairs[i+1] = a 
            my_pairs[i] = b 
            all_sorted = False 


print("\n\n")
print(my_pairs)

k = 1
idx2 = None
idx6 = None 

for i in range(len(my_pairs)):

    if my_pairs[i] == [[2]]:
        idx2 = k 
    
    elif my_pairs[i] == [[6]]:
        idx6 = k 

    k+= 1

print("\n\n")

for p in my_pairs:
    print(p)

        
print(idx2,idx6,idx2*idx6)
