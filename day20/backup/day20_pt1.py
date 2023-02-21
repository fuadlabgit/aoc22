# Day 20 part 1 
# groves coordinate 
import numpy as np 

input = """
1
2
-3
3
-2
0
4
"""

#with open("input.txt" ,"r") as file:
#    input = file.read()


input = input.strip().split("\n")
input = [int(i) for i in input]

print("input", input)

x = input 

"""
1 ---> 
2 --- > 
3
-3
4
"""

order = x.copy()

class Item:
    def __init__(self,val,prev,next):
        self.val = val 
        self.prev = prev 
        self.next = next 
    def __repr__(self):
        # return "<%s| %s |%s>" % (self.prev.val,self.val,self.next.val)
        return "<%s>" % (self.val)

class Ring:

    def __init__(self,items):
        self.items = items 
        self.first_item = items[0]

    def __repr__(self):
        return str(self.items)

    def sort(self):
         
        
        current = self.first_item 
        new_order = [current]

        for i in range(len(self.items)):
            if current.next != self.first_item:
                new_order.append(current.next)
            current = current.next 
        
        #print("sort", new_order)
        self.items = new_order 

    def mix(self,k):

        original_items = self.items.copy()
        
        i = 0
        while i <= k:
        
            next_item = original_items[i%len(original_items)]

            #print("mix next:",next_item.val)
            self.move(next_item)
            self.sort()
            # print("             " , self,"\n")
            i+= 1 

    def move(self,item):
        # 
        d = item.val 

        if np.sign(d) == +1:
            for i in range(d):
                self.move_right(item)
        elif np.sign(d) == -1:
            for i in range(-d):
                self.move_left(item)
        # else 0 


    def move_right(self,item):
        # move item right 
        # [p] [i] [x] [.] [n]
        #      |-------^
        
        i = item 
        p = item.prev 
        x = item.next 
        n = item.next.next 


        if item == self.first_item:
            self.first_item = x 
            # print("changed first item", x.val)
            

        i.prev = x 
        i.next = n 

        p.next = x 
        # p.prev does not change

        x.prev = p 
        x.next = i 

        n.prev = i 
        # np.next does not change 

    def move_left(self,item):
        # move item left 
        # [p] [.] [x] [i] [n]
        #      ^-------|

        i = item 
        x = item.prev 
        p = item.prev.prev 
        n = item.next 

        if item == self.first_item:
            self.first_item = n 

        i.prev = p 
        i.next = x
        
        n.prev = x 
        # n.next does not cange 

        x.next = n 
        x.prev = i 

        p.next = i 
        #p.prev does not change 


items = [Item(xi,None,None) for xi in x]


for i,item in enumerate(items):

    if i == 0:
        item.prev = items[-1]
        item.next = items[i+1]
    
    if i == len(items) -1:
        item.prev = items[i-1]
        item.next = items[0]
    
    else:
        item.prev = items[i-1]
        item.next = items[i+1]

print("initial arrangement", items)

ring = Ring(items)
first_item = items[0]

ring.mix(6)
print(ring)
val1 = first_item.next.val


"""
HINT what is the '1000th' number after zero ?

Initial arrangement:
1, 2, -3, 3, -2, 0, 4               <<<< HERE IT IS 4 ?

1 moves between 2 and -3:
2, 1, -3, 3, -2, 0, 4

2 moves between -3 and 3:
1, -3, 2, 3, -2, 0, 4

-3 moves between -2 and 0:
1, 2, 3, -2, -3, 0, 4

3 moves between 0 and 4:
1, 2, -2, -3, 0, 3, 4                     <<<<< HERE IT IS 3  ?

-2 moves between 4 and 1:
1, 2, -3, 0, 3, 4, -2

0 does not move:
1, 2, -3, 0, 3, 4, -2

4 moves between -3 and 0:
1, 2, -3, 4, 0, 3, -2

"""