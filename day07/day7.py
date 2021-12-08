print("--- DAY 7 ---")
print("--- PART 1 ---")

with open('input.txt') as f:
    crabs = [int(x) for x in f.readline().split(',')]

# Sort the crabs, the median is the least amount of total
# fuel required
crabs = sorted(crabs)
median = crabs[len(crabs)//2]
# sum the distances from the crabs' positions to the median
fuel_cost = sum(abs(x - median) for x in crabs)

print(f"The alignment position is {median} which takes "
      f"this much fuel: {fuel_cost}.")


print("--- DAY 7 ---")
print("--- PART 2 ---")


# Now we take into account the extra cost for moving farther,
# which will weight the outliers more.
# the cost function for the i-th step away is i*(i+1)/2
def cost(steps):
    return steps*(steps + 1)//2


# the mean weights the outliers, we potentially have a float here
# so we cast it to int and test which side has lower fuel cost
mean = int(sum(crabs) / len(crabs))
fuel_cost = sum(cost(abs(x-mean)) for x in crabs)
fuel_cost2 = sum(cost(abs(x-mean-1)) for x in crabs)
if fuel_cost2 < fuel_cost:
    mean += 1
    fuel_cost = fuel_cost2

print(f"The alignment position is {mean} which takes "
      f"this much fuel: {fuel_cost}.")
