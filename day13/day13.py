print("--- DAY 13 ---")
print("--- PART 1 ---")

# Store the points as a list
points = []
folds = []
with open('input.txt') as f:
    for line in f:
        # fold along x=655
        if line[:4] == "fold":
            if line[11] == "x":
                 folds.append((int(line[13:]), 0))
            else:
                 folds.append((0, int(line[13:])))
        try:
            x, y = line.strip().split(',')
            points.append((int(x), int(y)))
        except:
            # Blank line
            pass


def fold(arr, line):
    """Folds the input point array along the given line."""
    # Store a new output array
    out = []
    if line[0] == 0:
        # y-fold, go up
        val = line[1]
        for point in arr:
            if point[1] > val:
                # (val - (point - val))
                newy = 2*val - point[1]
            else:
                newy = point[1]
            out.append((point[0], newy))
    elif line[1] == 0:
        # x-fold, go left
        val = line[0]
        for point in arr:
            if point[0] > val:
                newx = 2*val - point[0]
            else:
                newx = point[0]
            out.append((newx, point[1]))
    return out


first_fold = fold(points, folds[0])

print(f"There are {len(set(first_fold))} many points after the first fold.")


print("--- DAY 13 ---")
print("--- PART 2 ---")

for f in folds:
    points = fold(points, f)


def print_board(points):
    """Prints the text in the points array."""
    max_x = 0
    max_y = 0
    for p in points:
        max_x = max(max_x, p[0])
        max_y = max(max_y, p[1])

    # max_x, max_y is our board size
    board = []
    for i in range(max_y + 1):
        board.append([' ' for _ in range(max_x + 1)])

    for p in points:
        board[p[1]][p[0]] = '#'
    
    for row in board:
        print("".join(x for x in row))

print_board(points)
