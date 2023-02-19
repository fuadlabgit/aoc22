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

    print("\t"*t , "- Compare %s vs %s" % (left, right))

    is_right_order = None 

    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            print("\t"*(t+1) , "- Left side is smaller, so inputs are in right order")
            return True  # continue checking
        elif left == right:
            return None
        elif left > right:
            print("\t"*(t+1) , "- Right side is smaller, so inputs are NOT in right order")
            return False # wrong order    

    elif isinstance(left, list) and isinstance(right, list):
        
        m =  len(left)-1
        n =  len(right)-1

        for i in range(max(m+1,n+1)):

            if i > m and i <= n: # left runs out first
                print("\t"*(t+1) , "- Left side runs out -> right order")
                return True 
            elif i <= m and i > n: # right runs out first
                print("\t"*(t+1) , "- Right side runs out -> NOT right order")
                return False 
            else:
                is_right_order = compare(left[i],right[i],t+1)
                
                if is_right_order is not None:
                    return is_right_order

        
    elif isinstance(left,list) and isinstance(right,int):
        print("\t"*(t+1) , "- Mixed types; convert right to %s and retry comparison" % [right])
        return compare(left,[right],t+1)
    
    elif isinstance(left,int) and isinstance(right,list):
        print("\t"*(t+1) , "- Mixed types; convert left to %s and retry comparison" % [left])
        return compare([left],right,t+1)
    

    return is_right_order



i = 1
indices = []

for line in input:
    pair_left = eval(line.split("\n")[0])
    pair_right = eval(line.split("\n")[1])

    print("== Pair %i ==" %i )
    print(pair_left,pair_right)
    success = compare(pair_left,pair_right)
    print("IS RIGHT ORDER?", success)
    if success:
        indices.append(i)
    i+=1

    print("\n")

print("indices",indices)
count = sum(indices)
print("COUNT", count )
