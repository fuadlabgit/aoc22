# Day 4, part 1

#lines = """
#2-4,6-8
#2-3,4-5
#5-7,7-9
#2-8,3-7
#6-6,4-6
#2-6,4-8
#""".strip().split("\n")

with open("input.txt","r") as file:
    lines = file.readlines()


score = 0

for line in lines:

    linesplit = line.split(",")
    
    part1 = linesplit[0] # 2-4
    part2 = linesplit[1] # 2-3

    one_split = part1.split("-")
    two_split = part2.split("-")

    # (a,b), (c,d)

    a = int(one_split[0])
    b = int(one_split[1])
    c = int(two_split[0])
    d = int(two_split[1])

    ab = set(range(a,b+1))
    cd = set(range(c,d+1))

    # if ab.issubset(cd) or cd.issubset(ab):
    #    score += 1

    # part 2 
    if not ab.intersection(cd) == set():
        score += 1

print(score)


    






