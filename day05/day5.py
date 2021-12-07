print("--- DAY 5 ---")
print("--- PART 1 ---")

lines = []
with open('input.txt') as f:
    for line in f:
        start, end = line.split('->')
        startx, starty = [int(x) for x in start.strip().split(',')]
        endx, endy = [int(x) for x in end.strip().split(',')]
        lines.append((startx, starty, endx, endy))

# Keep track of all (x, y) points in a dictionary lookup
# This saves a bit of space compared to storing the full array size,
# but still seems pretty inefficient.
# I gave some thought to storing separate dictionaries for x and y
# and then storing the to/from points there, but that would have been
# quite a bit trickier to take care of the cases of all the overlaps
# and multiple iterations.
points = dict()
for line in lines:
    x0, y0, x1, y1 = line
    if x0 == x1:
        # Horizontal line
        # Note the line could go either way, so just take
        # min/max for this
        for y in range(min(y0, y1), max(y0, y1) + 1):
            # Add it to the dictionary if it isn't present
            # and increment the count
            points.setdefault((x0, y), 0)
            points[(x0, y)] += 1
    elif y0 == y1:
        # Vertical line
        for x in range(min(x0, x1), max(x0, x1) + 1):
            points.setdefault((x, y0), 0)
            points[(x, y0)] += 1
    # Otherwise it is a diagonal line

# Now sum up the number of points that have 2 or greater values
total_overlap = 0
for point, count in points.items():
    if count > 1:
        total_overlap += 1

print(f"There are {total_overlap} points that overlap.")

print("--- DAY 5 ---")
print("--- PART 2 ---")

points = dict()
for line in lines:
    x0, y0, x1, y1 = line
    if x0 == x1:
        # Horizontal line
        # Note the line could go either way, so just take
        # min/max for this
        for y in range(min(y0, y1), max(y0, y1) + 1):
            # Add it to the dictionary if it isn't present
            # and increment the count
            points.setdefault((x0, y), 0)
            points[(x0, y)] += 1
    elif y0 == y1:
        # Vertical line
        for x in range(min(x0, x1), max(x0, x1) + 1):
            points.setdefault((x, y0), 0)
            points[(x, y0)] += 1
    else:
        # Otherwise it is a diagonal line
        npts = abs(x1 - x0)
        # We need to make sure we go in the right direction
        # for x and y
        xdir = 1 if x0 < x1 else -1
        ydir = 1 if y0 < y1 else -1
        for i in range(npts+1):
            x = x0 + i*xdir
            y = y0 + i*ydir
            points.setdefault((x, y), 0)
            points[(x, y)] += 1

# Now sum up the number of points that have 2 or greater values
total_overlap = 0
for point, count in points.items():
    if count > 1:
        total_overlap += 1

print(f"There are {total_overlap} points that overlap with diagonals.")
