print("--- DAY 9 ---")
print("--- PART 1 ---")

floor = []
with open('input.txt') as f:
    for line in f:
        row = [int(x) for x in line.strip()]
        floor += [row]

nrows = len(floor)
ncols = len(floor[0])

low_points = []
risk = 0
for i in range(nrows):
    for j in range(ncols):
        val = floor[i][j]
        # Top
        if i > 0 and val >= floor[i-1][j]:
            continue
        # Bottom
        if i < nrows - 1 and val >= floor[i+1][j]:
            continue
        # Left
        if j > 0 and val >= floor[i][j-1]:
            continue
        # Right
        if j < ncols - 1 and val >= floor[i][j+1]:
            continue
        # The value is lower than all of its neighbors, so
        # it is a low point
        low_points += [(i, j)]
        risk += 1 + val

print(f"There are {len(low_points)} low points, "
      f"with a risk factor of {risk}.")


print("--- DAY 9 ---")
print("--- PART 2 ---")


def traverse(to, visited):
    """
    Calculate the size of a basin recursively starting
    from the low point. Keep track of what nodes we've
    already visited so we don't double count and loop
    back on ourselves too.
    """
    i, j = to
    # We've already visited this node
    if to in visited:
        return 0
    visited += [to]
    val = floor[i][j]
    if val == 9:
        return 0
    this_sum = 1

    # Top
    if i > 0 and val < floor[i-1][j]:
        this_sum += traverse((i-1, j), visited)
    # Bottom
    if i < nrows - 1 and val < floor[i+1][j]:
        this_sum += traverse((i+1, j), visited)
    # Left
    if j > 0 and val < floor[i][j-1]:
        this_sum += traverse((i, j-1), visited)
    # Right
    if j < ncols - 1 and val < floor[i][j+1]:
        this_sum += traverse((i, j+1), visited)
    return this_sum


basin_sizes = []
for point in low_points:
    basin_sizes += [traverse(point, list())]

total = 1
for x in sorted(basin_sizes)[-3:]:
    total *= x

print(f"The multiplied total of the three largest basins: {total}")
