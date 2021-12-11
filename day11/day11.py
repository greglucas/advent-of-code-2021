print("--- DAY 11 ---")
print("--- PART 1 ---")

# Octopuses or octopii? ;)
octopuses = []

with open('input.txt') as f:
    for line in f:
        octopuses.append([int(x) for x in line.strip()])


def step():
    # 1) Add one energy to every octopus
    for i in range(10):
        for j in range(10):
            octopuses[i][j] += 1

    # 2) step through and see if any of the octopus should flash
    # adding the neighbors to the stack to keep track of
    has_flashed = [[False for i in range(10)] for j in range(10)]
    stack = [(i, j) for i in range(10) for j in range(10)]
    while len(stack) > 0:
        i, j = stack.pop()
        if octopuses[i][j] <= 9 or has_flashed[i][j]:
            # It didn't flash or has already flashed
            continue
        # This octopus has flashed, so process it
        has_flashed[i][j] = True
        for ii in [-1, 0, 1]:
            newi = i + ii
            for jj in [-1, 0, 1]:
                newj = j + jj
                if newi == i and newj == j:
                    # The current octopus
                    continue
                if newi < 0 or newj < 0 or newi > 9 or newj > 9:
                    # Out of bounds
                    continue
                octopuses[newi][newj] += 1
                # Add this neighbor octopus to the stack to check again
                stack.append((newi, newj))

    # 3) iterate through and take all octopii that flashed and
    # set them to 0
    flashes = 0
    for i in range(10):
        for j in range(10):
            if has_flashed[i][j]:
                flashes += 1
                octopuses[i][j] = 0
    return flashes


def print_board():
    for oct in octopuses:
        print("".join(str(x) for x in oct))


total_flashes = 0
for i in range(100):
    total_flashes += step()
    # For testing
    # print(f"After step {i+1}")
    # print_board()
print(f"There are {total_flashes} flashes after 100 steps.")


print("--- DAY 11 ---")
print("--- PART 2 ---")

octopuses = []
with open('input.txt') as f:
    for line in f:
        octopuses.append([int(x) for x in line.strip()])

flashes = 0
i = 0
while flashes != 100:
    i += 1
    flashes = step()

print(f"The octopuses synchronize after step {i}.")
