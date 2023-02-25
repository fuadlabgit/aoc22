# Day 24 


"""
1954 Barcelona A84
"""

import numpy as np 


def snafu_to_decimal(y):
    """
    converts a snafu code to decimal
    """

    d_fwd = {"=": -2, "-": -1, "0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9}

    x = 0

    N = len(y) 
    for i,yi in enumerate(y):
        x+= d_fwd[yi] * 5**(N-i-1)

    return x

def add_snafus(x,y):
    """
    adds two snafus x, y and returns the result as snafu
    """

    ptr = 0

    """
    0000000
          ^ ptr 
    
    ptr + 1 < ptr  > ptr - 1
    """

    d_fwd = {"=": -2, "-": -1, "0": 0, "1": 1, "2": 2} 
    d_bck = {-2: "=", -1: "-",0:"0",1:"1", 2:"2"}

    buf = [0]*(len(x))

    while ptr <= len(x) - 1:

        a = d_fwd[x[len(x) - 1 - ptr]]
        b = d_fwd[y[len(y) - 1 - ptr]]
        z = a + b 
        # print("a,b", a, b )
        
        if z > 2:
            z -= 5
            buf[len(buf) - 1 - ptr-1] += 1
        
        elif z < -2:
            z += 5
            buf[len(buf) - 1 -ptr-1] -= 1
        
        buf[len(buf) - 1 -ptr] += z 

        ptr += 1

        
    # return digits back to snafu encoding 
    z = "".join([d_bck[b] for b in buf])

    return z



    

def decimal_to_snafu(x):
    """
    converts a decimal number to snafu code
    """

    cache = {0: "0",1: "1",2: "2",3: "1=",4: "1-",5: "10",6: "11",7: "12",8: "2=", 9: "2-",}

    fac = int(np.log(x)//np.log(5)) # greatest divisor 
    
    number = x 
    snafus = []

    i = 0 
    while True:
        n = 5**(fac-i) # determine divisor for this iteration
        y = x//n

        M = fac-i

        if y > 0:
            # 1. look up digit in cache
            
            new_digits =  "0" + (i+2-len(cache[y])) * "0" + cache[y] + M * "0" 
            snafus.append(new_digits)

            # 2. update current number
            x -= n*y             
            if x <= 0 or fac-i < 0:
                break;

        i+= 1

    # print("snafus", snafus)
    # [print(i) for i in snafus]

    if len(snafus) > 1:
        """
        add up all the individual snafus
        """
        z =  add_snafus(snafus[0],snafus[1]) 

        k = 1
        while k < len(snafus) -1:
            z = add_snafus(z,snafus[k+1])
            k+= 1 
        
        return z 

    else:
        return snafus[0]



# 10: "20",
# 15: "1=0",
# 20: "1-0",
# 2022: "1=11-2",
# 12345: "1-0---0",
# 314159265: "1121-1110-1=0"

"""
print(snafu_to_decimal("1=11-2"))
print(snafu_to_decimal("1-0---0"))
print(snafu_to_decimal("1121-1110-1=0"))
print(decimal_to_snafu(314159265,cache))
"""


lines = """
1=-0-2
12111
  2=0=
    21
  2=01
   111
 20012
   112
 1=-1=
  1-12
    12
    1=
   122
""".split("\n")



with open("input.txt", "r") as file:
    lines = file.readlines()


# step 1: add all numbers
x = 0
for line in lines :
    print("line" ,line)
    x += snafu_to_decimal(line.strip())

print("x",x)

# step 2: convert result back to snafu 
r = decimal_to_snafu(x).lstrip("0") # remove leading zeros with lstrip
print(r)



