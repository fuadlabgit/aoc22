# Day 25 pt 1

input = """
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
122"""


input = input.strip().split("\n")


digits = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2
}


def snafu_to_decimal(x):
    # forward conversion
    x = str(x)

    N = len(x)

    c = 0
    for i,digit in enumerate(x):
        val = 5**(N-1-i)
        s = digits[digit]
        c+= val * s

    # print("snafu", x, "decimal", c)
    return c


def decimal_to_snafu(x):
    # backward conversion
    x = int(x)

    done = False
    i = 0
    while not done:
        fact = 5**(i)

        print("divide by", fact,x/fact)

        if x*1.0/fact < 1:
            done = True

        i+= 1


for d in [2022]: # [1,2,3,4,5,6,7,8,9,10,15,20,2022,12345,314159265]:
    snf = decimal_to_snafu(d)
    print("decimal", d, "snafu", snf)


"""
cumu = 0

for row in input:
    c = snafu_to_decimal(row)
    print("snafu", row, "decimal", c)

    cumu += c

print(cumu)
"""
