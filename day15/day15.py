import sys
sys.setrecursionlimit(100000)
print("--- DAY 15 ---")
print("--- PART 1 ---")

board = []
with open('input.txt') as f:
    for line in f:
        board.append(list(int(x) for x in line.strip()))

nrows = len(board)
ncols = len(board[0])

# Known maximum we can reach is if the entire board is 9s
# Taking all right and then all down steps
maxval = (nrows + ncols)*9

# A board to keep track of the minimum value it took to get to this
# spot. If we reach this location with a higher value, we know we can
# return back as that isn't the best path.
min_board = [[maxval for _ in range(ncols)] for _ in range(nrows)]

def traverse(i, j, total):
    """Traverse the maze from this position."""
    if i < 0 or j < 0 or i == nrows or j == ncols:
        # Out of bounds
        return maxval

    # Add this position to our total
    total += board[i][j]

    if total >= min_board[i][j]:
        # We know that this path isn't as good as one
        # we've already visited
        return maxval
    
    if i == nrows - 1 and j == ncols - 1:
        # We are at the exit
        return total

    min_board[i][j] = total

    # We want to return the minimum of all of our options
    # for directions
    return min([traverse(i+1, j, total),
               traverse(i-1, j, total),
               traverse(i, j+1, total),
               traverse(i, j-1, total)])

# We have implemented this with a depth-first search algorithm
# where we will keep traversing until we hit dead-ends or the
# finish. We've made it slightly faster by keeping track of the
# minimum distance to get to each node as we go, but it still
# doesn't help a whole lot. This is still a slow solution!
print("This may take a little while!")
print(traverse(0, 0, -board[0][0]))

print("--- DAY 15 ---")
print("--- PART 2 ---")

def expand_board(board):
    """Expand the board out 5x in each dimension."""
    newboard = [[0 for i in range(5*ncols)] for j in range(5*nrows)]
    # i, j are the multipliers
    for i in range(5):
        for j in range(5):
            # jj, ii are the original board iterators
            for jj in range(nrows):
                for ii in range(ncols):
                    iloc = ii + i*ncols
                    jloc = jj + j*nrows
                    val = board[jj][ii] + i + j
                    if val > 9:
                        # Wrap back to 1 if it is greater than 10
                        val -= 9
                    newboard[jloc][iloc] = val

    return newboard

board = expand_board(board)
nrows = len(board)
ncols = len(board[0])
maxval = (nrows + ncols)*9
min_board = [[maxval for _ in range(ncols)] for _ in range(nrows)]

# Use the same algorithm and just let it run since we don't really
# want to spend the time thinking of A* search algorithms. It has
# been a long time since I've thought of those, so I was happy to get
# the solution, albeit not optimized at all.
print(traverse(0, 0, -board[0][0]))
