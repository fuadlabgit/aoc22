
# Day 20 part 1
# groves coordinate
import numpy as np
from collections import deque

input = """
1
2
-3
3
-2
0
4
"""

with open("input.txt" ,"r") as file:
    input = file.read()


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

# 5962
# assert len(list(set(x))) == len(list(x)), len(list(x)) - len(list(set(x)))
# duplicate entries in the input data

x = [xi * 811589153 for xi in x]


class MyVal:

    counter = 0
    zero = None

    def __init__(self,val):
        self.val = val
        self.id_number = self.__class__.counter
        self.__class__.counter  += 1

        if self.val == 0:
            self.__class__.zero = self

    def __eq__(self,other):
        if self.val == other.val and self.id_number == other.id_number:
            return True
        return False

    def __add__(self,other):
        return MyVal(self.val + other.val)

    def __repr__(self):
        return str(self.val)

x = [MyVal(xi) for xi in x]
zero = MyVal.zero

d = deque(x)
order = list(x).copy()

def rotate_to_number(o):
    found = False
    k = 0

    while not found:
        d.rotate()
        k+= 1
        if d[0] == o:
            found = True

    return k

def mix(idx=0):

    print("start mixing...")
    L = len(order)
    for i in range(L):
        if i % 1000 ==0:
            print("progress", i/L)

        o = order[idx % len(order)]
        old_idx = d.index(o)

        if not o == zero:
            k = rotate_to_number(o)

            my_element = d.popleft()

            d.rotate(-o.val)
            d.appendleft(my_element)
            # d.rotate((old_idx + o) % len(order))

        idx += 1

    print("rotate to zero")
    rotate_to_number(zero)
    print("done.")
    return d[1],idx

idx = 0
for i in range(10):
    _,idx = mix(idx)

d.rotate(1)

N = -1000

d.rotate(N)
n1 = d[1]

d.rotate(N)
n2 = d[1]

d.rotate(N)
n3 = d[1]

print(n1)
print(n2)
print(n3)

print("---------")
print(n1 + n2 + n3)
