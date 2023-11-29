

# part 1 

with open("input.txt","r") as file:
    lines = file.readlines()


elves = []

calories = 0

for line in lines:
    # print(line)

    if line == "\n":
        elves.append(calories)
        calories = 0
    
    else:
        calories += int(line)


# print(elves)
print("Part 1:", max(elves))



# part 2 

elves = sorted(elves)
# [3,1,4] -> [1,3,4]

top_elves_calories = elves[-1]  + elves[-2] + elves[-3]

print("Part 2: ", top_elves_calories)
