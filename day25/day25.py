print("--- DAY 25 ---")
print("--- PART 1 ---")

seafloor = list()
with open("input.txt") as f:
    for line in f:
        row = [x if x != "." else None for x in line.strip()]
        seafloor.append(row)

def print_seafloor(seafloor):
    for row in seafloor:
        print("".join([x if x is not None else "." for x in row]))

# print_seafloor(seafloor)
nrows = len(seafloor)
ncols = len(seafloor[0])


def can_move(seafloor, i, j):
    testi, testj = i, j
    if seafloor[i][j] == ">":
        testj += 1
        if testj == ncols:
            # Handle the wrap
            testj = 0
    elif seafloor[i][j] == "v":
        testi += 1
        if testi == nrows:
            # Handle the wrap
            testi = 0
    else:
        # There is no cucumber here
        return False
    
    if seafloor[testi][testj] is None:
        # Can only move if the location is empty
        return True
    return False

def move(seafloor):
    # Move all east facing cucumbers first, then the south
    updated = False
    for east_south in ">v":
        # Keep track of which elements to move
        should_move = list()
        for i in range(nrows):
            for j in range(ncols):
                if seafloor[i][j] == east_south and can_move(seafloor, i, j):
                    should_move.append((i, j))
        if len(should_move) > 0:
            # This means we did move some elements
            updated = True
        for loc in should_move:
            # Iterate through the list of elements that can move this step
            i, j = loc
            newi, newj = i, j
            if east_south == ">":
                newj += 1
            else:
                # V
                newi += 1
            if newi == nrows:
                newi = 0
            if newj == ncols:
                newj = 0
            seafloor[newi][newj] = seafloor[i][j]
            seafloor[i][j] = None

    return seafloor, updated

updated = True
moves = 0
while updated:
    seafloor, updated = move(seafloor)
    moves += 1

print_seafloor(seafloor)
print(moves)
