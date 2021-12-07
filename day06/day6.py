print("--- DAY 6 ---")
print("--- PART 1 ---")

with open('input.txt') as f:
    fish = [int(x) for x in f.readline().split(',')]

# Take a step each day
for day in range(80):
    # Iterate over all fish updating them properly
    for i in range(len(fish)):
        fish[i] -= 1
        if fish[i] < 0:
            # It produces a new fish
            fish.append(8)
            # and resets to 6
            fish[i] = 6

print(f"There are {len(fish)} lanternfish after 80 days.")


print("--- DAY 6 ---")
print("--- PART 2 ---")

# Now we need to rethink how we calculate, we can't just append
# to the end of the list each time. Lets try keeping track of
# how many fish are in each day of their evolution instead.

with open('input.txt') as f:
    fish = [int(x) for x in f.readline().split(',')]

evolution = [0]*9
for f in fish:
    evolution[f] += 1

# Take a step each day
for day in range(256):
    # Iterate over all fish updating them properly
    reproducers = evolution[0]
    for i in range(8):
        evolution[i] = evolution[i+1]
    # Put the reproducers back to 6
    evolution[6] += reproducers
    # And create their children
    evolution[8] = reproducers

print(f"There are {sum(evolution)} lanternfish after 80 days.")
